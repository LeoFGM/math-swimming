
from constants import GameState
import random
from random import randint
from pgzero.keyboard import keyboard

class BackgroundManager:
    SCROLL_INCREMENT = 0.0003
    MAX_SCROLL = 600

    def __init__(self):
        self.scroll = 0
        self.neg = 1
        self.backgrounds = []

    def set_background(self, screen):
        screen.clear()
        for i in range(3):
            bg = screen.blit("river", (0, i * (600 * self.neg) + self.scroll))
            self.backgrounds.append(bg)
            self.neg = -1

    def moving_bg(self):
        for _ in self.backgrounds:
            self.scroll += self.SCROLL_INCREMENT
        if abs(self.scroll) > self.MAX_SCROLL:
            self.scroll = 0

class ActorMovementManager:
    DEFAULT_POSITIONS = [250, 400, 550]

    def __init__(self):
        pass

    def move_swimmer(self, actor, objects, normal_speed, fast_speed):
        if keyboard.left and actor.x > 190:
            actor.x -= fast_speed if objects else normal_speed
        if keyboard.right and actor.x < 625:
            actor.x += fast_speed if objects else normal_speed

    def reposition_actors(self, game_actors, *actors, quantity, special_effect=None, alt_quantity=None):
        flattened_actors = [actor for actor_group in actors for actor in (actor_group if isinstance(actor_group, list) else [actor_group])]
        for actor in flattened_actors:
            if not hasattr(actor, "special_x") or actor.special_x is None:
                actor.special_x = None

            actor.x_positions = actor.x_positions or self.DEFAULT_POSITIONS
            actor.random_x_range = (190, 625)

            if actor.y < 630:
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

    def reset_actors_position(self, *actors):
        flattened_actors = [actor for actor_group in actors for actor in (actor_group if isinstance(actor_group, list) else [actor_group])]
        for actor in flattened_actors:
            actor.y = randint(actor.first, actor.last)

class CollisionManager:
    def __init__(self, actor_animation):
        self.actor_animation = actor_animation
        self.last_collision = 0

    def handle_all_collisions(self, excluded_actor):
        valid_actors = {}
        for name, actor in self.actor_animation.moving_actors.items():
            if isinstance(actor, list):
                for i, item in enumerate(actor):
                    valid_actors[f"{name}_{i}"] = item
            else:
                valid_actors[name] = actor

        for name1, actor1 in valid_actors.items():
            if name1 != excluded_actor:
                for name2, actor2 in valid_actors.items():
                    if name1 != name2 and (name1 != excluded_actor or name2 != excluded_actor) and actor1.colliderect(actor2):
                        self.collision_action(name1, actor1, name2, actor2)

    def collision_action(self, name1, actor1, name2, actor2):
        size1 = actor1.width * actor1.height
        size2 = actor2.width * actor2.height

        is_swimmer1 = 'swimmer' in name1
        is_swimmer2 = 'swimmer' in name2
        if not is_swimmer1 and not is_swimmer2:
            if size1 < size2:
                actor1.y += 50
            elif size2 < size1:
                actor2.y += 50

    def q_block_collision(self, current_screen, game_actors, game_questions, q_screen):
        if game_actors.swimmer.colliderect(game_actors.q_block):
            game_actors.q_block.y = randint(-2000, -1600)
            current_screen = GameState.QUESTION_TIME
            game_questions.question_screen = q_screen
        return current_screen

    def log_collision(self, game_actors, game_clocks, sounds, ts):
        for log in game_actors.logs:
            if game_actors.swimmer.colliderect(log) and ts - self.last_collision >= 3:
                game_clocks.count_max += 3
                game_clocks.score -= 3
                self.last_collision = ts
                sounds.hit.play()
                self.actor_animation.not_hit = False

    def speed_powerup_collision(self, game_actors, game_clocks, new_music, duration, initial_music, music_actions, clock):
        for powerup in game_actors.powerups:
            if game_actors.swimmer.colliderect(powerup) and 'speed' in powerup.image:
                game_actors.powerup_collision = True
                game_clocks.count_max -= 5
                clock.schedule(game_actors.stop_powerup, 5)
                game_clocks.start_timer()
                powerup.pos = (random.choice(ActorMovementManager.DEFAULT_POSITIONS), randint(-2000, -1600))
                music_actions.change_music_temporarily(new_music, duration, initial_music)

    def score_powerup_collision(self, game_actors, game_clocks, sounds, clock):
        for powerup in game_actors.powerups:
            if game_actors.swimmer.colliderect(powerup) and 'score' in powerup.image:
                sounds.score_powerup.set_volume(0.5)
                sounds.score_powerup.play()
                game_actors.powerup_collision = True
                powerup.pos = (random.choice(ActorMovementManager.DEFAULT_POSITIONS), randint(-2000, -1600))
                clock.schedule_unique(game_actors.stop_powerup, 5.0)
                game_clocks.start_timer()

    def coin_collision(self, game_actors, game_clocks, sounds):
        for coin in game_actors.coins:
            if game_actors.swimmer.colliderect(coin):
                game_clocks.score += 2 if game_actors.powerup_collision else 1
                sounds.coin.play()
                coin.pos = (randint(175, 625), randint(-800, -200))

    def shark_collision(self, game_actors, game_clocks, sounds):
        if game_actors.shark.colliderect(game_actors.swimmer) and game_actors.shark.image != "shark_14":
            game_clocks.count_max += 3
            sounds.sharkbite.set_volume(0.5)
            sounds.sharkbite.play()
            game_actors.shark.image = "shark_14"
            game_actors.shark.pos = (random.choice(ActorMovementManager.DEFAULT_POSITIONS), randint(-800, -500))

    def poop_collision(self, game_actors, game_clocks, sounds):
        if game_actors.swimmer.colliderect(game_actors.poop):
            game_clocks.score -= 5
            sounds.hit.set_volume(0.5)
            sounds.hit.play()
            game_actors.poop.pos = (-5000, -5000)

    def glasses_collision(self, game_actors, game_clocks, current_screen, sounds):
        if game_actors.swimmer.colliderect(game_actors.glasses):
            if 'speed' in current_screen.value:
                game_clocks.count_max -= 1
            elif 'points' in current_screen.value:
                game_clocks.score += 2
            sounds.angelical.set_volume(0.25)
            sounds.angelical.play()
            game_actors.glasses.pos = random.choice(ActorMovementManager.DEFAULT_POSITIONS), randint(game_actors.glasses.first, game_actors.glasses.last)

class ActorMovementInteractions:
    def __init__(self, actor_animation):
        self.background_manager = BackgroundManager()
        self.actor_movement_manager = ActorMovementManager()
        self.collision_manager = CollisionManager(actor_animation)
        self.DEFAULT_POSITIONS = ActorMovementManager.DEFAULT_POSITIONS
        self.backgrounds = self.background_manager.backgrounds

    def set_background(self, screen):
        self.background_manager.set_background(screen)

    def moving_bg(self):
        self.background_manager.moving_bg()

    def move_swimmer(self, actor, objects, normal_speed, fast_speed):
        self.actor_movement_manager.move_swimmer(actor, objects, normal_speed, fast_speed)

    def reposition_actors(self, game_actors, *actors, quantity, special_effect=None, alt_quantity=None):
        self.actor_movement_manager.reposition_actors(game_actors, *actors, quantity=quantity, special_effect=special_effect, alt_quantity=alt_quantity)

    def reset_actors_position(self, *actors):
        self.actor_movement_manager.reset_actors_position(*actors)

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