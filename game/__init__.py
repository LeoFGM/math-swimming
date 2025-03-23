from .actors import GameActors, ActorMovementInteractions, AnimationManager, CompActors
from .changevar import GameClocks
from .levels import (
    speedrun_level_easy,
    points_level_easy,
    speedrun_level_medium,
    points_level_medium
)

from .questions import GameQuestions
from .screens import Screen, MenuScreens, GameScreens, GameOverScreens, QuestionScreens
from .settings import settings
from .musicals import MusicalActions

# Define what is exposed when someone imports the package
__all__ = [
    'GameActors',
    'ActorMovementInteractions',
    'AnimationManager',
    'CompActors',
    'GameClocks',
    'speedrun_level_easy',
    'points_level_easy',
    'speedrun_level_medium',
    'points_level_medium',
    'GameQuestions',
    'Screen',
    'MenuScreens',
    'GameScreens',
    'GameOverScreens',
    'QuestionScreens',
    'settings',
    'MusicalActions'
]