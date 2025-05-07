import pygame

from .transitions import TransitionManager, Screen
from ..core.context import GameContext


class GameScreens(Screen):
    def __init__(self, game_actors, transition_manager=None):
        self.text_color = "orange red"
        super().__init__(game_actors, transition_manager)

    def update_game_screen(self, game_state, context: GameContext(), level_function, *args):
        context.movement.moving_bg()
        transition_result = self.transition_manager.update(1/60)
        if transition_result:
            return transition_result

        return level_function(*args)

    def _draw_timer_info(self, screen, timers, x=20, y=60):
        y_offset = y
        for timer_name, timer_data in timers.items():
            remaining = int(timer_data['remaining'])
            text = self._get_timer_text(timer_name, remaining)
            if text:
                screen.draw.text(text, topleft=(x, y_offset), fontsize=30, color=self.text_color)
                y_offset += 30

    def _get_timer_text(self, timer_name, remaining):
        timer_texts = {
            "inversion": f"Inversed for: {remaining}s",
            "speed_powerup": f"Speed boost: {remaining}s",
            "push_powerup": f"Push power: {remaining}s",
            "score_powerup": f"Points doubled: {remaining}s",
            "magnet_powerup": f"Attract objects for: {remaining}s"
        }
        return timer_texts.get(timer_name)

    def draw_speedrun_easy_screen(self, screen, context):
        context.movement.set_background(screen)
        context.actors.swimmer.draw()
        context.actors.draw_category('special', 'q_block', 'inversion_portal')
        context.actors.draw_category('powerups')
        context.actors.draw_category('obstacles', 'logs')
        context.actors.draw_category('collectibles', 'glasses')
        screen.draw.text(f"Time: {int(context.clock.count_max)}", color=self.text_color, topleft=(20, 20), fontsize=40)
        self._draw_timer_info(screen, context.clock.active_timers)
        self.transition_manager.draw(screen)

    def draw_points_easy_screen(self, screen, context):
        context.movement.set_background(screen)
        context.actors.swimmer.draw()
        context.actors.draw_category('special')
        context.actors.draw_category('obstacles', 'logs')
        context.actors.draw_category('collectibles', 'coins', 'glasses')
        context.actors.draw_category('powerups')
        screen.draw.text(f"Time: {context.clock.count_down_max}", color=self.text_color, topleft=(20, 20), fontsize=40)
        screen.draw.text(f"Score: {context.clock.score}", color=self.text_color, topleft=(660, 20), fontsize=40)
        self._draw_timer_info(screen, context.clock.active_timers)
        if context.actors.magnet_active:
            # Draw magnetic field effect
            radius = 200 * (0.9 + 0.1 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
            screen.draw.filled_circle(
                (context.actors.swimmer.x, context.actors.swimmer.y),
                radius,
                (100, 200, 255, 30)  # Semi-transparent blue
            )

    def draw_speedrun_medium_screen(self, screen, context: GameContext()):
        context.movement.set_background(screen)
        context.actors.swimmer.draw()
        if context.comp_actors.bird_attack_active:
            context.actors.draw_category('bird_attack')
        else:
            context.actors.draw_category('special')
            context.actors.draw_category('obstacles', 'logs', 'shark')
            context.actors.draw_category('collectibles', 'glasses', 'swimmer_cap')
            context.actors.draw_category('powerups')
        screen.draw.text(f"Time: {int(context.clock.count_max)}", color=self.text_color, topleft=(20, 20), fontsize=40)

        if context.clock.shield > 0:
            shield_x = 660
            shield_y = 60
            screen.draw.text("Shield count:", topleft=(660, shield_y - 20), fontsize=30, color=self.text_color)
            for i in range(min(context.clock.shield, 3)):
                screen.blit('shield', (shield_x + (i * 40), shield_y))

        self._draw_timer_info(screen, context.clock.active_timers)

    def draw_points_medium_screen(self, screen, context: GameContext()):
        context.movement.set_background(screen)
        context.actors.swimmer.draw()
        if context.comp_actors.bird_attack_active:
            context.actors.draw_category('bird_attack')
        else:
            context.actors.draw_category('special')
            context.actors.draw_category('obstacles', 'bear', 'poop', 'logs')
            context.actors.draw_category('collectibles')
            context.actors.draw_category('powerups')
        screen.draw.text(f"Time: {int(context.clock.count_down_max)}", color=self.text_color, topleft=(20, 20), fontsize=40)
        screen.draw.text(f"Score: {context.clock.score}", color=self.text_color, topleft=(660, 20), fontsize=40)
        context.comp_actors.pooping(context)

        self._draw_timer_info(screen, context.clock.active_timers)

        if "pooping_time" in context.comp_actors.poop_pos:
            context.actors.obstacles['poop'].draw()

        if context.clock.shield > 0:
            shield_x = 660
            shield_y = 80
            screen.draw.text("Shield count:", topleft=(660, shield_y - 20), fontsize=30, color=self.text_color)
            for i in range(min(context.clock.shield, 3)):
                screen.blit('shield', (shield_x + (i * 40), shield_y))