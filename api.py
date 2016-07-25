# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""

import string
import logging
import endpoints
from protorpc import remote, messages, message_types
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import User, Game, Score, Ranking
from models import StringMessage, NewGameForm, GameForm, GameForms, MakeMoveForm,\
    ScoreForms, RankingForm, RankingForms, HistoryForm
from utils import get_by_urlsafe


NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)
CANCEL_GAME_REQUEST = endpoints.ResourceContainer(
        user_name=messages.StringField(1),
        urlsafe_game_key=messages.StringField(2))
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1),)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))
MEMCACHE_MOVES_REMAINING = 'MOVES_REMAINING'


@endpoints.api(name='hangman', version='v1')
class HangmanAPI(remote.Service):
    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        game = Game.new_game(user.key, request.attempts)

        # Use a task queue to update the average attempts remaining.
        # This operation is not needed to complete the creation of a new game
        # so it is performed out of sequence.
        taskqueue.add(url='/tasks/cache_average_attempts')
        return game.to_form('Good luck playing Hangman!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=CANCEL_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}/cancel',
                      name='cancel_game',
                      http_method='POST')
    def cancel_game(self, request):
        """Cancel a user's active game."""
        user = User.query(User.name == request.user_name).get()
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            return game.to_form('This game is already over!')
        if not user:
            raise endpoints.NotFoundException( 
                    'A user with that name does not exist!')
        if user.key != game.user:
            raise endpoints.ForbiddenException(
                    'You cannot cancel a game that is not your own!')
        else:
            # Cancelled games can't be high on the 'leaderboard'.
            game.end_game(False)
            game.key.delete()
        return game.to_form('This game has been canceled.')

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=GameForms,
                      path='game/user/{user_name}',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Returns all of an individual User's games."""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name unfortunately does not exist!')
        games = Game.query(Game.user == user.key)
        return GameForms(items=[game.to_form(message="Here are the games.")\
                                for game in games])

    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """Makes a move. Returns a game state with message"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            return game.to_form('Game already over!')

        if request.guess in game.already_guessed:
            return game.to_form('You have already guessed these letters: {}'\
                                .format(game.already_guessed))
        
        game.already_guessed.append(request.guess)

        indexes_of_correct = [i for i, g in enumerate(game.target)\
                              if g == request.guess]

        if not indexes_of_correct:
            game.attempts_remaining -= 1
            # Display the 'board' with the message
            msg = string.join(game.board, '')
            msg += ' Not in word. You have {} attempts remaining.'.format(\
                        game.attempts_remaining)
        else:
            for i in indexes_of_correct:
                game.board[i] = request.guess
            msg = string.join(game.board, '')
            msg += ' You got one!'
        
        game.history.append({'guess': request.guess,
                             'board': string.join(game.board, ''),
                             'already_guessed': game.already_guessed})
        
        if string.join(game.board, '') == game.target:
            game.end_game(True)
            msg = string.join(game.board, '')
            return game.to_form(msg + ' You win!')

        if game.attempts_remaining < 1:
            game.end_game(False)
            return game.to_form(msg + ' Game over!')
        else:
            game.put()
            return game.to_form(msg)

    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=ScoreForms,
                      path='scores/user/{user_name}',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """Returns all of an individual User's scores"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        scores = Score.query(Score.user == user.key)
        return ScoreForms(items=[score.to_form() for score in scores])

    @endpoints.method(request_message=message_types.VoidMessage,
                      response_message=ScoreForms,
                      path='highscores',
                      name='get_high_scores',
                      http_method='GET')
    def get_high_scores(self, request):
        """Returns the top scores in decending order.
        TODO: Add a param number_of_results to limit
        returned results."""
        highscores = Score.query(Score.won == True).order(Score.incorrect_guesses).fetch()
        return ScoreForms(items=[highscore.to_form() for\
                                 highscore in highscores])


    @endpoints.method(request_message=USER_REQUEST,
                      response_message=RankingForm,
                      path='ranking/user/{user_name}',
                      name='get_user_ranking',
                      http_method='POST')
    def get_user_ranking(self, request):
        """Returns the performance of the player as a Ranking."""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        
        scores = Score.query(Score.user == user.key).fetch()
        if not scores:
            raise endpoints.NotFoundException(
                    'No scores were found for that user!')
        
        wins = sum(s.won == True for s in scores)
        percent_won = (float(wins)/len(scores)) * 100
        number_of_guesses = sum(score.incorrect_guesses for score in scores)
        avg_wrong = float(number_of_guesses)/len(scores)

        ranking = Ranking.query(Ranking.user == user.key).get()
        if ranking:
            ranking.wins = wins
            ranking.percent_won = percent_won
            ranking.avg_wrong = avg_wrong
            ranking.put()
            return ranking.to_form("Ranking has been updated for {}".format(\
                                        user.name))
        else:
            ranking = Ranking.new_ranking(user=user.key,
                                          wins=wins,
                                          percent_won=percent_won,
                                          avg_wrong=avg_wrong)
            return ranking.to_form("Ranking created for {}".format(user.name))
 
    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=HistoryForm,
                      path='history/game/{urlsafe_game_key}',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Produces a history of the guesses of a game."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        return game.to_history_form()

    @endpoints.method(response_message=StringMessage,
                      path='games/average_attempts',
                      name='get_average_attempts_remaining',
                      http_method='GET')
    def get_average_attempts(self, request):
        """Get the cached average moves remaining"""
        return StringMessage(message=memcache.get(MEMCACHE_MOVES_REMAINING) or '')

    @staticmethod
    def _cache_average_attempts():
        """Populates memcache with the average moves remaining of Games"""
        games = Game.query(Game.game_over == False).fetch()
        if games:
            count = len(games)
            total_attempts_remaining = sum([game.attempts_remaining
                                            for game in games])
            average = float(total_attempts_remaining)/count
            memcache.set(MEMCACHE_MOVES_REMAINING,
                         'The average moves remaining is {:.2f}'.format(average))


api = endpoints.api_server([HangmanAPI])
