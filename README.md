# Hangman Game API

## Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered
in the App Engine admin console and would like to use to host your instance of hangman.
2.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's
running by visiting the API Explorer - by default localhost:8080/_ah/api/explorer.
3.  (Optional) Generate your client library(ies) with the endpoints tool. Deploy
your application.
 
## Game Description:
Hangman is a guessing game. Each game begins with a random 'target' word taken
from a list of zoo animals in wordbank.py, as well as a maximum number of
'attempts.' A 'guess' is sent to the `make_move` endpoint which will reply with
the 'board' (stars [*] represent a blank for each letter of the word), and with
the message 'You got one!', 'Not in word!', 'game over', or 'you win!' Many different
Hangman games can be played by many different users at any given time. Each game
can be retrieved or played using the path parameter `urlsafe_game_key`.

### Keeping Score:
When a game ends, a score is created for the user playing that game. The score
records how many incorrrect guesses were given, whether the player won or not,
and the date of the game. You can view scores and high scores using the scores
endpoints documented below.

## Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - index.yaml: Contains auto-generated indices for composite queries to the 
 datastore.
 - LICENSE: Do what you will with this software. :)
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.
 - wordbank.py: Module contains a function that returns a random string for use
 as the target in a Hangman game.

## Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a User with that user_name already exists.
    
 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user_name, attempts
    - Returns: GameForm with initial game state.
    - Description: Creates a new Game. user_name provided must correspond to an
    existing user - will raise a NotFoundException if not. Also adds a task to
    a task queue to update the average moves remaining for active games.
     
 - **get_game**
    - Path: 'game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: GameForm with current game state.
    - Description: Returns the current state of a game.

 - **cancel_game**
    - Path: 'game/{urlsafe_game_key}/cancel'
    - Method: DELETE
    - Parameters: urlsafe_game_key
    - Returns: GameForm with game state and a message confirming cancellation.
    - Description: Cancels a currently active game.

 - **get_user_games**
    - Path: 'game/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: GameForms containing a specific users games.
    - Description: Returns the requested user's games.

 - **make_move**
    - Path: 'game/{urlsafe_game_key}'
    - Method: PUT
    - Parameters: urlsafe_game_key, guess
    - Returns: GameForm with new game state.
    - Description: Accepts a 'guess' in the form of a single alphabetic
    character and returns the updated state of the game. If this causes a game
    to end, a corresponding Score entity will be created.
    
 - **get_scores**
    - Path: 'scores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns all Scores in the database (unordered).
    
 - **get_user_scores**
    - Path: 'scores/user/{user_name}'
    - Method: GET
    - Parameters: user_name
    - Returns: ScoreForms. 
    - Description: Returns all Scores recorded by the provided player (unordered).
    Will raise a NotFoundException if the User does not exist.

 - **get_high_scores**
    - Path: 'highscores'
    - Method: GET
    - Parameters: None
    - Returns: ScoreForms.
    - Description: Returns winning scores in the database ordered by least
    incorrect guesses.

 - **get_user_ranking** 
    - Path: 'ranking/user/{username}'
    - Method: GET
    - Parameters: user_name
    - Returns: RankingForm.
    - Description: Returns a ranking for a player based on the performance of
    previous games.
    
 - **get_game_history**
    - Path: 'history/game/{urlsafe_game_key}'
    - Method: GET
    - Parameters: urlsafe_game_key
    - Returns: HistoryForm
    - Description: Returns a games history of moves made.

## Models Included:
 - **User**
    - Stores unique user_name and (optional) email address.
    
 - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.

 - **Ranking**
    - Stores a user's ranking. Associated with User model via
    KeyProperty.
    
 - **Score**
    - Records completed games. Associated with Users model via KeyProperty.
    
## Forms Included:
 - **GameForm**
    - Representation of a Game's state (urlsafe_key, attempts_remaining,
    game_over flag, message, user_name).
 - **GameForms**
    - Multiple GameForm container.
 - **NewGameForm**
    - Used to create a new game (user_name, min, max, attempts)
 - **MakeMoveForm**
    - Inbound make move form (guess).
 - **ScoreForm**
    - Representation of a completed game's Score (user_name, date, won flag,
    guesses).
 - **ScoreForms**
    - Multiple ScoreForm container.
 - **RankingForm**
    - Representation of a player's ranking (user_name, wins, percent_won, avg_wrong).
 - **RankingForms**
    - Multiple RankingForm container.
 - **StringMessage**
    - General purpose String container.