# -*- coding: utf-8 -*-`
"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb
from wordbank import randomWord


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()


class Game(ndb.Model):
    """Game object"""
    target = ndb.StringProperty(required=True)
    attempts_allowed = ndb.IntegerProperty(required=True, default=6)
    attempts_remaining = ndb.IntegerProperty(required=True, default=6)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    board = ndb.JsonProperty(required=True)
    already_guessed = ndb.JsonProperty(required=True)
    history = ndb.JsonProperty(required=True)

    @classmethod
    def new_game(cls, user, attempts):
        """Creates and returns a new game"""
        target = randomWord()
        game = Game(user=user,
                    target=target,
                    attempts_allowed=attempts,
                    attempts_remaining=attempts,
                    board=['*' for char in target],
                    already_guessed=[],
                    history=[],
                    game_over=False)
        game.put()
        return game


    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.message = message
        return form

    def to_history_form(self):
        return HistoryForm(history=str(self.history))

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won,
                      incorrect_guesses=self.attempts_allowed - self.attempts_remaining)
        score.put()


class Ranking(ndb.Model):
    """Ranking object"""
    user = ndb.KeyProperty(required=True, kind='User')
    wins = ndb.IntegerProperty(required=True)    
    percent_won = ndb.FloatProperty(required=True) 
    avg_wrong = ndb.FloatProperty(required=True)   

    @classmethod
    def new_ranking(cls, user, wins, percent_won, avg_wrong):
        """Creates and returns a new ranking"""
        ranking = Ranking(user=user,
                          wins=wins,
                          percent_won=percent_won,
                          avg_wrong=avg_wrong)
        ranking.put()
        return ranking

    def to_form(self, message):
         form = RankingForm()
         form.user_name = self.user.get().name
         form.wins = self.wins
         form.percent_won = self.percent_won
         form.avg_wrong = self.avg_wrong
         form.message = message
         return form


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    incorrect_guesses = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date), incorrect_guesses=self.incorrect_guesses)


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    attempts_remaining = messages.IntegerField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    user_name = messages.StringField(5, required=True)


class GameForms(messages.Message):
    """Return multiple GameForms"""
    items = messages.MessageField(GameForm, 1, repeated=True)
    

class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)
    attempts = messages.IntegerField(2, default=6)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    guess = messages.StringField(1, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    incorrect_guesses = messages.IntegerField(4, required=True)

class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)


class RankingForm(messages.Message):
    """Ranking Form for outbound Ranking information"""
    user_name = messages.StringField(1, required=True)
    wins = messages.IntegerField(2)
    percent_won = messages.FloatField(3)
    avg_wrong = messages.FloatField(4)
    message = messages.StringField(5)

 
class RankingForms(messages.Message):
    """Return multiple Ranking forms"""
    items = messages.MessageField(RankingForm, 1, repeated=True)


class HistoryForm(messages.Message):
    """History form for outbound history information"""
    history = messages.StringField(1)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
