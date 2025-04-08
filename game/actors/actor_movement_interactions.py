import time

import random
from random import randint
from pgzero.keyboard import keyboard

from game.actors.collision_manager import CollisionManager


class BackgroundManager:
    SCROLL_INCREMENT = 1
    MAX_SCROLL = 600

    def __init__(self):
        self.scroll = 0
        self.neg = 1
        self.backgrounds = []
        self.is_inverted = False

    def set_background(self, screen):
        screen.clear()
        bg_image = "river_inverted" if self.is_inverted else "river"
        self.backgrounds = []
        for i in range(3):
            y_pos = i * (600 * self.neg) + self.scroll
            bg = screen.blit(bg_image, (0, y_pos))
            self.backgrounds.append(bg)
            self.neg = -1

    def toggle_inversion(self):
        self.is_inverted = not self.is_inverted

    def moving_bg(self):
        self.scroll += self.SCROLL_INCREMENT
        if abs(self.scroll) > self.MAX_SCROLL:
            self.scroll = 0


class ActorMovementManager:

    def __init__(self):
        pass

    def move_swimmer(self, actor_animation, actor, objects, normal_speed, fast_speed):
        current_speed = fast_speed if objects else normal_speed
        if keyboard.left:
            if actor_animation.inversion_active:
                if actor.x < 625:
                    actor.x += current_speed
            else:
                if actor.x > 190:
                    actor.x -= current_speed

        if keyboard.right:
            if actor_animation.inversion_active:
                if actor.x > 190:
                    actor.x -= current_speed
            else:
                if actor.x < 625:
                    actor.x += current_speed

    def reposition_actors(self, game_actors, actor_animation, dt, *actors, quantity, special_effect=None, alt_quantity=None):
        flattened_actors = [actor for actor_group in actors for actor in (actor_group if isinstance(actor_group, list) else [actor_group])]
        for actor in flattened_actors:
            if not hasattr(actor, "special_x") or actor.special_x is None:
                actor.special_x = None

            if hasattr(actor, 'is_being_pushed') and actor.is_being_pushed:
                self.update_push_animation(actor, game_actors, dt)
                continue

            actor.x_positions = actor.x_positions or CollisionManager.DEFAULT_POSITIONS
            actor.random_x_range = (190, 625)

            if actor_animation.inversion_active:
                actor.y -= alt_quantity if special_effect else quantity
            elif actor.y < 630 and not actor_animation.inversion_active:
                actor.y += alt_quantity if special_effect else quantity
            else:
                if 'log' in actor.image:
                    new_y, new_x = self.logs_reposition(game_actors, actor)
                elif actor.use_random_choice:
                    new_x = random.choice(actor.x_positions)
                elif actor.special_x is not None:
                    new_x = actor.special_x
                else:
                    new_x = randint(*actor.random_x_range)
                new_y = randint(actor.first, actor.last)
                actor.pos = (new_x, new_y)

    def logs_reposition(self, game_actors, log):
        max_attempts = 50
        for _ in range(max_attempts):
            log.y = randint(-800, -500)
            if all(abs(log.y - other_log.y) > 200 for other_log in game_actors.logs if other_log != log):
                break
        else:
            log.y = -800
        return log.y, log.x

    def reset_actors_position(self, actor_animation, *actors):
        flattened_actors = [actor for actor_group in actors for actor in (actor_group if isinstance(actor_group, list) else [actor_group])]
        for actor in flattened_actors:
            if actor_animation.inversion_active:
                actor.y = randint(200 + (-1 * actor.last), 200 + (-1 * actor.first))
            else:
                actor.y = randint(actor.first, actor.last)

    def update_push_animation(self, log, game_actors, dt):
        if not hasattr(log, 'is_being_pushed') or not log.is_being_pushed:
            return False

        elapsed = time.time() - log.push_start_time
        duration = 1.0

        if elapsed >= duration:
            self._complete_push_animation(log)
            return False

        progress = min(elapsed/duration, 1.0)
        x_progress =  progress
        y_progress = progress * (2 - progress)


        x_offset = 700 * x_progress
        y_offset = -400 * (1 - (2*y_progress-1)**2)

        if not hasattr(log, 'push_direction'):
            log.push_direction = 1 if log.x < game_actors.swimmer.x else -1


        log.x = log.original_pos[0] + (x_offset * log.push_direction)
        log.y = log.original_pos[1] + y_offset

        return True


    def _complete_push_animation(self, log):
        if hasattr(log, 'is_being_pushed'):
            log.x = log.original_pos[0]
            log.y = randint(-800, -500)

            for attr in ['is_being_pushed', 'push_start_time', 'original_pos', 'push_direction']:
                if hasattr(log, attr):
                    delattr(log, attr)


class ActorMovementInteractions:
    def __init__(self, actor_animation, transition_manager=None):
        self.background_manager = BackgroundManager()
        self.actor_movement_manager = ActorMovementManager()
        self.collision_manager = CollisionManager(
            actor_animation,
            self.background_manager,
            transition_manager,
            self.actor_movement_manager
        )
        self.DEFAULT_POSITIONS = CollisionManager.DEFAULT_POSITIONS
        self.transition_manager = transition_manager

    def set_background(self, screen):
        self.background_manager.set_background(screen)

    def moving_bg(self):
        self.background_manager.moving_bg()

    def move_swimmer(self, actor_animation, actor, objects, normal_speed, fast_speed):
        self.actor_movement_manager.move_swimmer(actor_animation, actor, objects, normal_speed, fast_speed)

    def reposition_actors(self, game_actors, actor_animation, dt, *actors, quantity, special_effect=None, alt_quantity=None):
        self.actor_movement_manager.reposition_actors(game_actors, actor_animation, dt, *actors, quantity=quantity, special_effect=special_effect, alt_quantity=alt_quantity)

    def update_push_animation(self, log, game_actors, dt):
        self.actor_movement_manager.update_push_animation(log, game_actors, dt)

    def reset_actors_position(self, actor_animation, *actors):
        self.actor_movement_manager.reset_actors_position(actor_animation, *actors)

    def handle_all_collisions(self, excluded_actor):
        self.collision_manager.handle_all_collisions(excluded_actor)

    def q_block_collision(self, current_screen, game_actors, game_questions, q_screen):
        return self.collision_manager.q_block_collision(current_screen, game_actors, game_questions, q_screen)

    def log_collision(self, game_actors, game_clocks, sounds, ts):
        self.collision_manager.log_collision(game_actors, game_clocks, sounds, ts)

    def speed_powerup_collision(self, game_actors, game_clocks, new_music, duration, initial_music, music_actions, clock):
        self.collision_manager.speed_powerup_collision(game_actors, game_clocks, new_music, duration, initial_music, music_actions, clock)

    def score_powerup_collision(self, game_actors, game_clocks, sounds, clock):
        self.collision_manager.score_powerup_collision(game_actors, game_clocks, sounds, clock)

    def coin_collision(self, game_actors, game_clocks, sounds):
        self.collision_manager.coin_collision(game_actors, game_clocks, sounds)

    def shark_collision(self, game_actors, game_clocks, sounds):
        self.collision_manager.shark_collision(game_actors, game_clocks, sounds)

    def poop_collision(self, game_actors, game_clocks, sounds):
        self.collision_manager.poop_collision(game_actors, game_clocks, sounds)

    def glasses_collision(self, game_actors, game_clocks, current_screen, sounds):
        self.collision_manager.glasses_collision(game_actors, game_clocks, current_screen, sounds)

    def inversion_portal_collision(self, game_actors, game_clocks, actor_animation, transition_manager, sounds, *actors):
        self.collision_manager.inversion_portal_collision(game_actors, game_clocks, actor_animation, transition_manager, sounds, *actors)

    def push_powerup_collision(self, game_actors, game_clocks, sounds):
        self.collision_manager.push_powerup_collision(game_actors, game_clocks, sounds)

