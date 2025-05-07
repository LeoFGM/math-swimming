from .transitions import TransitionManager, Screen
from game.core import settings

class MenuScreens(Screen):

    def __init__(self, game_actors):
        super().__init__(game_actors)

    def update_static_screen(self, actor_animation, actor_movement, current_screen):
        actor_animation.static_update_animations()
        actor_movement.scroll = 0
        transition_result = self.transition_manager.update(1/60)
        if transition_result:
            return transition_result
        return current_screen

    def draw_start_screen(self, screen):
        self.game_actors.draw_category('menu', 'start', 'gamename')

    def draw_gamemode_screen(self, screen):
        self.game_actors.draw_category('menu', 'gamemode', 'speedrun', 'pointsmania', 'goback')

    def draw_difficulty_screen(self, screen):
        self.game_actors.draw_category('menu', 'difficulty', 'easy', 'medium', 'hard', 'extreme', 'goback')


