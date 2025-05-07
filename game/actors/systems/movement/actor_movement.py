import random
import time
from random import randint
from pgzero.keyboard import keyboard

from game.actors.systems.collision import CollisionManager
from game.core.context import GameContext


class ActorMovementManager:
    def __init__(self, config=None):
        self.config = config or {
            "default_positions": [250, 400, 550],
            "collision_cooldown": 3,
            "powerup_duration": 5}

    def move_swimmer(self, context, objects, normal_speed, fast_speed):
        current_speed = fast_speed if objects else normal_speed


        if keyboard.left:
            if context.animation.inversion_active:
                if context.player.x < 625:
                    context.player.x += current_speed
            else:
                if context.player.x > 190:
                    context.player.x -= current_speed

        if keyboard.right:
            if context.animation.inversion_active:
                if context.player.x > 190:
                    context.player.x -= current_speed
            else:
                if context.player.x < 625:
                    context.player.x += current_speed

        if context and getattr(context.comp_actors, 'bird_attack_active', False):
            if keyboard.up:
                context.player.y = max(300, context.player.y - current_speed)
            if keyboard.down:
                context.player.y = min(550, context.player.y + current_speed)

    def reposition_actors(self, context, dt, *actors, quantity, special_effect=None,
                          alt_quantity=None):
        # Get all actors including logs
        all_actors = []
        for actor_group in actors:
            if actor_group == context.actors.logs or (
                    isinstance(actor_group, list) and any(a in context.actors.logs for a in actor_group)):
                all_actors.extend(context.actors.logs)
            elif isinstance(actor_group, list):
                all_actors.extend(actor_group)
            else:
                all_actors.append(actor_group)

        for actor in all_actors:
            # Skip if being pushed
            if hasattr(actor, 'is_being_pushed') and actor.is_being_pushed:
                self.update_push_animation(actor, context, dt)
                continue


            move_amount = alt_quantity if special_effect else quantity
            if context.comp_actors.bird_attack_active or 'bear' in actor.image or 'poop' in actor.image:
                continue
            else:
                if context.animation.inversion_active:
                    move_amount = -abs(move_amount)  # Force negative during inversion
                else:
                    move_amount = abs(move_amount)  # Force positive normally

            actor.y += move_amount
            if (not context.animation.inversion_active and actor.y > 630) or \
                    (context.animation.inversion_active and actor.y < -1000):
                self.reset_actors_position(context, actor)



    def reset_actors_position(self, context, *actors):
        flattened_actors = [actor for actor_group in actors for actor in
                            (actor_group if isinstance(actor_group, list) else [actor_group])]
        for actor in flattened_actors:
            # Position Y
            if context.animation.inversion_active:
                actor.y = randint(200 + (-1 * actor.last), 200 + (-1 * actor.first))
            else:
                actor.y = randint(actor.first, actor.last)

            # Position X
            if 'log' in actor.image:
                actor.x = actor.special_x if hasattr(actor, 'special_x') else actor.x
            elif getattr(actor, 'use_random_choice', False):
                x_positions = getattr(actor, 'x_positions', None)
                actor.x = random.choice(x_positions) if x_positions else actor.x
            elif hasattr(actor, 'special_x') and actor.special_x is not None:
                actor.x = actor.special_x
            else:
                actor.x = randint(190, 625)

    def update_push_animation(self, log, context, dt):
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
            log.push_direction = 1 if log.x < context.player.x else -1


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

    #Magnet logic:

    def update_magnet_effect(self, context, dt):
        if not getattr(context.actors, 'magnet_powerup_active', False):
            return

        magnet_strength = 0.15 * dt * 60
        magnet_radius = 200

        for coin in context.actors.coins:
            if self.distance_to(context.player, coin) < magnet_radius:
                coin.x += (context.player.x - coin.x) * magnet_strength
                coin.y += (context.player.y - coin.y) * magnet_strength

        if hasattr(context.actors.collectibles, 'glasses'):
            glasses = context.actors.collectibles['glasses']
            if self.distance_to(context.player, glasses) < magnet_radius:
                glasses.x += (context.player.x - glasses.x) * magnet_strength
                glasses.y += (context.player.y - glasses.y) * magnet_strength

    def distance_to(self, actor1, actor2):
        return ((actor1.x - actor2.x)**2 + (actor1.y - actor2.y)**2)**0.5

