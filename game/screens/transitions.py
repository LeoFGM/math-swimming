import pygame
from game.core import settings

class Screen:
    def __init__(self, game_actors, transition_manager=None):
        self.game_actors = game_actors
        self.transition_manager =  transition_manager or TransitionManager()

    def draw(self, screen, game_clocks, actor_movement):
        self.transition_manager.draw(screen)
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, dt, actor_animation, actor_movement, current_screen):
        transition_result = self.transition_manager.update(dt)
        if transition_result:
            return transition_result
        return current_screen


class TransitionManager:
    def __init__(self):
        self.flash_surface = None
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

        #Powerups animation
        self.powerup_message_active = False
        self.powerup_message_text = ""
        self.powerup_message_image = None
        self.powerup_message_duration = 1.0
        self.powerup_message_progress = 0
        self.powerup_message_scale = 1.0
        self.max_scale = 2.0

    def update(self, dt):
        if self.transition_active:
            self.transition_progress += dt / self.transition_duration
            if self.should_switch and self.transition_progress >= 0.5:
                self.should_switch = False
                return self.next_screen

            elif self.transition_progress >= 1:
                self.transition_active = False

        if self.flash_active:
            self.flash_progress += dt
            if self.flash_progress >= self.flash_duration:
                self.flash_active = False
                if self.post_flash_action:
                    self.post_flash_action()

        if self.powerup_message_active:
            self.powerup_message_progress += dt / self.powerup_message_duration

            if self.powerup_message_progress < 0.3:
                self.powerup_message_scale = 1.0 + (self.max_scale - 1.0) * (self.powerup_message_progress / 0.3)
            elif self.powerup_message_progress > 0.7:
                self.powerup_message_scale = self.max_scale - (self.max_scale - 1.0) * ((self.powerup_message_progress - 0.7) / 0.3)

                if self.powerup_message_progress >= 1:
                    self.powerup_message_active = False

        return None

    def draw(self, screen):
        if self.powerup_message_active:
            alpha = int(255 * (1 - self.powerup_message_progress * 0.5))
            scale = self.powerup_message_scale

            if self.powerup_message_image:
                scaled_img = pygame.transform.scale(self.powerup_message_image, (int(self.powerup_message_image.get_width() * scale), int(self.powerup_message_image.get_height() * scale)))
                scaled_img.set_alpha(alpha)
                screen.blit(scaled_img, (settings.WIDTH// 2 - scaled_img.get_width()// 2, settings.HEIGHT// 2 - scaled_img.get_height()// 2 - 50))

            font = pygame.font.Font(None, int(36 * scale))
            text = font.render(self.powerup_message_text, True, (255, 255, 255))
            text.set_alpha(alpha)
            screen.blit(text, (settings.WIDTH// 2 - text.get_width()// 2, settings.HEIGHT// 2 + 50))

        if self.transition_active:
            alpha = int(
                510 * (self.transition_progress if self.transition_progress <= 0.5 else 1 - self.transition_progress))
            self.transition_surface.fill((0, 0, 0))
            self.transition_surface.set_alpha(alpha)
            screen.blit(self.transition_surface, (0, 0))

        if self.flash_active:
            progress = min(1.0, self.flash_progress / self.flash_duration)
            alpha = int(255 * (1 - abs(progress - 0.5) * 2))
            flash_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255))
            flash_surface.set_alpha(alpha)
            screen.blit(flash_surface, (0, 0))



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

    def show_powerup_message(self, message, image):
        self.powerup_message_active = True
        self.powerup_message_text = message
        self.powerup_message_image = image
        self.powerup_message_progress = 0
        self.powerup_message_scale = 1.0

