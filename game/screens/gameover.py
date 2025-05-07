from .transitions import Screen
from ..core.context import GameContext


class GameOverScreens(Screen):
    def draw_gameover_speed_screen(self, screen, settings, context: GameContext()):
        screen.draw.text(f"You completed the level in: {int(context.clock.level_elapsed_time)} seconds!", color="black", center=settings.CENTER, fontsize=60)
        context.actors.draw_category('menu', 'goback')

    def draw_gameover_points_screen(self, screen, settings, context: GameContext()):
        screen.draw.text(f"You ended with: {context.clock.score} points!", color="black", center=settings.CENTER, fontsize=60)
        context.actors.draw_category('menu', 'goback')