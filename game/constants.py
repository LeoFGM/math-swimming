from enum import Enum

class Screens:
    START = 'start'
    GAMEMODE = 'gamemode'
    DIFFICULTY_SPEED = 'difficulty_speed'
    DIFFICULTY_POINTS = 'difficulty_points'
    SPEEDRUN_EASY = 'speedrun_easy'
    POINTS_EASY = 'points_easy'
    SPEEDRUN_MEDIUM = 'speedrun_medium'
    POINTS_MEDIUM = 'points_medium'
    GAMEOVER_SPEED = 'gameover_speed'
    GAMEOVER_POINTS = 'gameover_points'
    QUESTION_TIME = 'question_time'

class QuestionStates:
    SPEED_EASY = 'speed_easy'
    POINTS_EASY = 'points_easy'
    SPEED_MEDIUM = 'speed_medium'
    POINTS_MEDIUM = 'points_medium'

class Answers:
    CORRECT = 'correct'
    INCORRECT = 'incorrect'

class GameState(Enum):
    START = Screens.START
    GAMEMODE = Screens.GAMEMODE
    DIFFICULTY_SPEED = Screens.DIFFICULTY_SPEED
    DIFFICULTY_POINTS = Screens.DIFFICULTY_POINTS
    SPEEDRUN_EASY = Screens.SPEEDRUN_EASY
    POINTS_EASY = Screens.POINTS_EASY
    SPEEDRUN_MEDIUM = Screens.SPEEDRUN_MEDIUM
    POINTS_MEDIUM = Screens.POINTS_MEDIUM
    GAMEOVER_SPEED = Screens.GAMEOVER_SPEED
    GAMEOVER_POINTS = Screens.GAMEOVER_POINTS
    QUESTION_TIME = Screens.QUESTION_TIME