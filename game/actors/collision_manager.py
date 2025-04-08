import random
from random import randint
from threading import Timer

from constants import GameState


class CollisionManager:
    DEFAULT_POSITIONS = [250, 400, 550]
    def __init__(self, actor_animation, background_manager, transition_manager=None, actor_movement_manager=None):
        self.actor_animation = actor_animation
        self.last_collision = 0
        self.background_manager = background_manager
        self.transition_manager = transition_manager
        self.actor_movement_manager = actor_movement_manager

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
                game_clocks.start_timer('speed_powerup', 5)
                clock.schedule_unique(lambda: game_actors.stop_powerup(game_clocks), 5)
                powerup.pos = (random.choice(self.DEFAULT_POSITIONS), randint(-2000, -1600))
                music_actions.change_music_temporarily(new_music, duration, initial_music)

    def score_powerup_collision(self, game_actors, game_clocks, sounds, clock):
        for powerup in game_actors.powerups:
            if game_actors.swimmer.colliderect(powerup) and 'score' in powerup.image:
                sounds.score_powerup.set_volume(0.5)
                sounds.score_powerup.play()
                game_actors.powerup_collision = True
                powerup.pos = (random.choice(self.DEFAULT_POSITIONS), randint(-2000, -1600))
                game_clocks.start_timer('score_powerup', 5)
                clock.schedule_unique(lambda : game_actors.stop_powerup(game_clocks), 5.0)


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
            game_actors.shark.pos = (random.choice(self.DEFAULT_POSITIONS), randint(-800, -500))

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
            sounds.whip.set_volume(0.5)
            sounds.whip.play()
            game_actors.glasses.pos = random.choice(self.DEFAULT_POSITIONS), randint(game_actors.glasses.first, game_actors.glasses.last)

    def inversion_portal_collision(self, game_actors, game_clocks, actor_animation, transition_manager, sounds, *actors):
        if game_actors.swimmer.colliderect(game_actors.inversion_portal):
            sounds.inversion.set_volume(0.5)
            sounds.inversion.play()
            game_actors.inversion_portal.pos = random.choice(self.DEFAULT_POSITIONS), randint(game_actors.inversion_portal.first, game_actors.inversion_portal.last)
            game_clocks.start_timer('inversion', 10)
            def after_flash():
                actor_animation.activate_inversion()
                self.background_manager.toggle_inversion()
                game_actors.swimmer.y = 50
                self.actor_movement_manager.reset_actors_position(actor_animation, *actors)

            if transition_manager is None:
                transition_manager = self.transition_manager

            transition_manager.start_flash(post_flash_action=after_flash)

    def push_powerup_collision(self, game_actors, game_clocks, sounds):
        for powerup in game_actors.powerups:
            if game_actors.swimmer.colliderect(powerup) and 'push' in powerup.image:
                sounds.p_powerup.play()
                game_actors.push_powerup_active = True
                game_clocks.start_timer('push_powerup', 5)
                powerup.pos = (random.choice(self.DEFAULT_POSITIONS), randint(-2000, -1600))
                t = Timer(5.0, game_actors.deactivate_push_powerup, args=(game_clocks,))
                t.start()
                for log in game_actors.logs:
                    if hasattr(log, 'is_being_pushed'):
                        if not hasattr(log, 'original_pos'):
                            log.original_pos = (log.x, log.y)