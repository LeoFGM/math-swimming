import pygame

from game.settings import settings


class TransitionManager:
    def __init__(self):
        self.transition_type = "fade"
        self.transition_progress = 0
        self.transition_duration = 1 # seconds
        self.transition_active = False
        self.transition_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)

        self.next_screen = None
        self.current_screen = None
        self.should_switch = False

        #Flash animation
        self.flash_duration = 0.3
        self.flash_active = False
        self.flash_progress = 0
        self.post_flash_action = None

    def start_flash(self, post_flash_action=None):
        self.flash_active = True
        self.flash_progress = 0
        self.post_flash_action = post_flash_action
        self.flash_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
        self.flash_surface.fill((255, 255, 255))

    def start_transition(self, next_screen):
        self.transition_progress = 0
        self.transition_active = True
        self.next_screen = next_screen
        self.should_switch = True
        self.transition_surface.fill((0, 0, 0))

    def update(self, dt):
        if self.transition_active:
            self.transition_progress += dt / self.transition_duration
            if self.should_switch and self.transition_progress >= 0.5:
                self.should_switch = False
                return self.next_screen

            elif self.transition_progress >= 1:
                self.transition_active = False

        elif self.flash_active:
            self.flash_progress += dt
            if self.flash_progress >= self.flash_duration:
                self.flash_active = False
                if self.post_flash_action:
                    self.post_flash_action()

        return None

    def draw(self, screen):
        if self.transition_active:
            alpha = int(
                510 * (self.transition_progress if self.transition_progress <= 0.5 else 1 - self.transition_progress))
            self.transition_surface.fill((0, 0, 0))  # Black for fade
            self.transition_surface.set_alpha(alpha)
            screen.blit(self.transition_surface, (0, 0))

            # Handle flash transition (separate check)
        elif self.flash_active:
            progress = min(1.0, self.flash_progress / self.flash_duration)
            alpha = int(255 * (1 - abs(progress - 0.5) * 2))
            flash_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255))  # White for flash
            flash_surface.set_alpha(alpha)
            screen.blit(flash_surface, (0, 0))

class Screen:
    def __init__(self, game_actors):
        self.game_actors = game_actors
        self.transition_manager = TransitionManager()

    def draw(self, screen, game_clocks, actor_movement):
        self.transition_manager.draw(screen)
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, dt, actor_animation, actor_movement, current_screen):
        transition_result = self.transition_manager.update(dt)
        if transition_result:
            return transition_result
        return current_screen


class MenuScreens(Screen):
    def update_static_screen(self, actor_animation, actor_movement, current_screen):
        actor_animation.static_update_animations()
        actor_movement.scroll = 0
        transition_result = self.transition_manager.update(1/60)
        if transition_result:
            return transition_result
        return current_screen

    def draw_start_screen(self, screen):
        self.game_actors.draw_actors(self.game_actors.start, self.game_actors.gamename)

    def draw_gamemode_screen(self, screen):
        self.game_actors.draw_actors(self.game_actors.speedrun, self.game_actors.pointsmania, self.game_actors.gamemode, self.game_actors.goback)

    def draw_difficulty_screen(self, screen):
        self.game_actors.draw_actors(self.game_actors.difficulty, self.game_actors.easy, self.game_actors.medium, self.game_actors.hard, self.game_actors.extreme, self.game_actors.goback)

class GameScreens(Screen):
    def __init__(self, game_actors):
        super().__init__(game_actors)

    def update_game_screen(self, game_state, actor_movement, level_function, *args):
        actor_movement.moving_bg()
        transition_result = self.transition_manager.update(1/60)
        if transition_result:
            return transition_result

        return level_function(*args)

    def draw_speedrun_easy_screen(self, screen, game_clocks, game_actors, actor_movement, actor_animation):
        actor_movement.set_background(screen)
        game_actors.draw_actors(game_actors.swimmer, game_actors.q_block, game_actors.glasses, game_actors.inversion_portal)
        game_actors.create_and_draw_actors(game_actors.logs, game_actors.powerups)
        screen.draw.text(f"Time: {game_clocks.count_max}", color="orange red", topleft=(20, 20), fontsize=40)
        y_offset = 60
        for timer_name, timer_data in game_clocks.active_timers.items():
            remaining = int(timer_data['remaining'])
            if timer_name == "inversion":
                screen.draw.text(f"Inversed for: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            elif timer_name == "speed_powerup":
                screen.draw.text(f"Speed boost: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            elif timer_name == "push_powerup":
                screen.draw.text(f"Push power: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            y_offset += 30
        self.transition_manager.draw(screen)

    def draw_points_easy_screen(self, screen, game_clocks, game_actors, actor_movement, actor_animation):
        actor_movement.set_background(screen)
        game_actors.draw_actors(game_actors.swimmer, game_actors.q_block, game_actors.glasses, game_actors.inversion_portal)
        game_actors.create_and_draw_actors(game_actors.logs, game_actors.coins)
        screen.draw.text(f"Time: {game_clocks.count_down_max}", color="orange red", topleft=(20, 20), fontsize=40)
        screen.draw.text(f"Score: {game_clocks.score}", color="orange red", topleft=(660, 20), fontsize=40)
        y_offset = 60
        for timer_name, timer_data in game_clocks.active_timers.items():
            remaining = int(timer_data['remaining'])
            if timer_name == "inversion":
                screen.draw.text(f"Inversed for: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            elif timer_name == "score_powerup":
                screen.draw.text(f"Points doubled: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            elif timer_name == "push_powerup":
                screen.draw.text(f"Push power: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            y_offset += 30

    def draw_speedrun_medium_screen(self, screen, game_clocks, game_actors, actor_movement, actor_animation):
        actor_movement.set_background(screen)
        game_actors.draw_actors(game_actors.swimmer, game_actors.q_block, game_actors.shark, game_actors.glasses, game_actors.inversion_portal)
        game_actors.create_and_draw_actors(game_actors.logs, game_actors.powerups)
        screen.draw.text(f"Time: {game_clocks.count_max}", color="orange red", topleft=(20, 20), fontsize=40)
        y_offset = 60
        for timer_name, timer_data in game_clocks.active_timers.items():
            remaining = int(timer_data['remaining'])
            if timer_name == "inversion":
                screen.draw.text(f"Inversed for: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            elif timer_name == "speed_powerup":
                screen.draw.text(f"Speed boost: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            elif timer_name == "push_powerup":
                screen.draw.text(f"Push power: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            y_offset += 30

    def draw_points_medium_screen(self, screen, game_clocks, game_actors, actor_movement, actor_animation, comp_actors):
        actor_movement.set_background(screen)
        game_actors.draw_actors(game_actors.swimmer, game_actors.q_block, game_actors.bear, game_actors.glasses, game_actors.inversion_portal)
        game_actors.create_and_draw_actors(game_actors.logs, game_actors.coins, game_actors.powerups)
        screen.draw.text(f"Time: {game_clocks.count_down_max}", color="orange red", topleft=(20, 20), fontsize=40)
        screen.draw.text(f"Score: {game_clocks.score}", color="orange red", topleft=(660, 20), fontsize=40)
        comp_actors.pooping(actor_animation)

        y_offset = 60
        for timer_name, timer_data in game_clocks.active_timers.items():
            remaining = int(timer_data['remaining'])
            if timer_name == "inversion":
                screen.draw.text(f"Inversed for: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            elif timer_name == "score_powerup":
                screen.draw.text(f"Points doubled: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            elif timer_name == "push_powerup":
                screen.draw.text(f"Push power: {remaining}s", topleft=(20, y_offset), fontsize=30, color="orange red")
            y_offset += 30

        if "pooping_time" in comp_actors.poop_pos:
            game_actors.poop.draw()



class QuestionScreens:

    def draw_question_screen(self, screen, game_questions):

        question_data = {
            'speed_easy': game_questions.question_e,
            'points_easy': game_questions.question_e,
            'speed_medium': game_questions.question_m,
            'points_medium': game_questions.question_m
        }


        if game_questions.question_screen in question_data:
            question = question_data[game_questions.question_screen]
            game_questions.draw_questions(screen, time_left=10, question=question)
        else:
            print(f"Error: Invalid question screen type: {game_questions.question_screen}")

class GameOverScreens(Screen):
    def draw_gameover_speed_screen(self, screen, settings, game_clocks, game_actors):
        screen.draw.text(f"You completed the level in: {int(game_clocks.level_elapsed_time)} seconds!", color="black", center=settings.CENTER, fontsize=60)
        game_actors.goback.draw()

    def draw_gameover_points_screen(self, screen, settings, game_clocks, game_actors):
        screen.draw.text(f"You ended with: {game_clocks.score} points!", color="black", center=settings.CENTER, fontsize=60)
        game_actors.goback.draw()