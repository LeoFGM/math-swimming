import random

from random import randint

from game.constants import GameState


class CollisionManager:
    def __init__(self, actor_animation, background_manager, config=None, transition_manager=None, actor_movement_manager=None):
        self.actor_animation = actor_animation
        self.last_collision = 0
        self.background_manager = background_manager
        self.transition_manager = transition_manager
        self.actor_movement_manager = actor_movement_manager
        self.config = config or {
            "default_positions": [250, 400, 550],
            "collision_cooldown": 3,
            "powerup_duration": 5
        }

    def handle_between_collisions(self, excluded_actor):
        game_actors = self.actor_animation.game_actors
        valid_actors = {}

        for name, actor in game_actors.obstacles.items():
            if name == 'logs':
                for i, log in enumerate(actor):
                    valid_actors[f"log_{i}"] = log
            else:
                valid_actors[name] = actor

        for name, actor in game_actors.collectibles.items():
            if name == 'coins':
                for i, coin in enumerate(actor):
                    valid_actors[f"coin_{i}"] = coin
            else:
                valid_actors[name] = actor

        for powerup in game_actors.powerups["powerups"]:
            valid_actors[f"powerup_{id(powerup)}"] = powerup

        for name, actor in game_actors.special.items():
            valid_actors[name] = actor

        valid_actors['swimmer'] = game_actors.swimmer

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

    def q_block_collision(self, context, q_screen):
        if context.player.colliderect(context.actors.special['q_block']):
            context.actors.special['q_block'].y = randint(-2000, -1600)
            context.questions.question_screen = q_screen
            context.clock.start_timer('question_timer', 10)
            return GameState.QUESTION_TIME
        return context.current_screen

    def log_collision(self, context, ts):
        for log in context.actors.obstacles['logs']:
            if context.player.colliderect(log) and ts - self.last_collision >= 3:
                if context.clock.shield > 0:
                    context.clock.shield -= 1
                    context.sounds.shield_hit.play()
                else:
                    self.collision_penalty(context, speed_penalty=2, points_penalty=2)
                    context.sounds.hit.play()
                self.last_collision = ts
                self.actor_animation.not_hit = False

    def speed_powerup_collision(self, context, new_music, duration, initial_music):
        for powerup  in context.actors.powerups["powerups"]:
            if 'speed_powerup' in powerup.image and context.player.colliderect(powerup):
                if self.transition_manager:
                    self.transition_manager.show_powerup_message("Move faster now!", powerup._surf)
                context.actors.speed_powerup_collision = True
                context.clock.count_max -= 5
                powerup.pos = (random.choice(self.config["default_positions"]), randint(-2000, -1600))
                context.audio.change_music_temporarily(new_music, duration, initial_music)

                def deactivate_speed():
                    context.actors.speed_powerup_collision = False

                context.clock.start_timer('speed_powerup', 5, deactivate_speed)

    def score_powerup_collision(self, context):
        for powerup  in context.actors.powerups["powerups"]:
            if 'score_powerup' in powerup.image and context.player.colliderect(powerup):
                if self.transition_manager:
                    self.transition_manager.show_powerup_message("Double points!", powerup._surf)
                context.sounds.score_powerup.set_volume(0.5)
                context.sounds.score_powerup.play()
                context.actors.score_powerup_collision = True
                powerup.pos = (random.choice(self.config["default_positions"]), randint(-2000, -1600))

                def deactivate_score():
                    context.actors.score_powerup_collision = False

                context.clock.start_timer('score_powerup', 5, deactivate_score)

    def coin_collision(self, context):
        for coin in context.actors.collectibles["coins"]:
            if context.player.colliderect(coin):
                context.clock.score += 2 if context.actors.score_powerup_collision else 1
                context.sounds.coin.play()
                coin.pos = (randint(175, 625), randint(-800, -200))

    def shark_collision(self, context):
        if context.actors.obstacles['shark'].colliderect(context.player) and context.actors.obstacles['shark'].image != "shark_14":
            if context.clock.shield > 0:
                context.clock.shield -= 1
                context.sounds.shield_hit.play()
            else:
                self.collision_penalty(context, speed_penalty=2, points_penalty=3)
                context.sounds.sharkbite.set_volume(0.5)
                context.sounds.sharkbite.play()
                self.actor_animation.not_hit = False
            context.actors.obstacles['shark'].image = "shark_14"
            context.actors.obstacles['shark'].pos = (random.choice(self.config["default_positions"]), randint(-800, -500))

    def poop_collision(self, context):
        if context.actors.swimmer.colliderect(context.actors.obstacles['poop']):
            if context.clock.shield > 0:
                context.clock.shield -= 1
                context.sounds.shield_hit.play()
            else:
                context.clock.score -= 5
                context.sounds.hit.set_volume(0.5)
                context.sounds.hit.play()
            context.actors.obstacles['poop'].pos = (-5000, -5000)

    def glasses_collision(self, context):
        if context.actors.swimmer.colliderect(context.actors.collectibles['glasses']):
            self.collision_bonus(context, speed_bonus=1, points_bonus=2)
            context.sounds.whip.set_volume(0.5)
            context.sounds.whip.play()
            context.actors.collectibles['glasses'].pos = random.choice(self.config["default_positions"]), randint(context.actors.collectibles['glasses'].first, context.actors.collectibles['glasses'].last)

    def collision_bonus(self, context, speed_bonus=None, points_bonus=None):
        if 'speed' in context.current_screen.value:
            context.clock.count_max -= speed_bonus
        elif 'points' in context.current_screen.value:
            context.clock.score += points_bonus

    def collision_penalty(self, context, speed_penalty=None, points_penalty=None):
        if 'speed' in context.current_screen.value:
            context.clock.count_max += speed_penalty
        elif 'points' in context.current_screen.value:
            context.clock.score -= points_penalty

    def inversion_portal_collision(self, context, *actors):
        if context.player.colliderect(context.actors.special['inversion_portal']):
            context.sounds.inversion.set_volume(0.5)
            context.sounds.inversion.play()
            context.actors.special['inversion_portal'].pos = random.choice(self.config["default_positions"]), randint(context.actors.special['inversion_portal'].first, context.actors.special['inversion_portal'].last)
            context.clock.start_timer('inversion', 10)
            def after_flash():
                if self.actor_movement_manager:
                    self.actor_movement_manager.reset_actors_position(context, *actors)
                context.animation.activate_inversion()
                self.background_manager.toggle_inversion()
                context.player.y = 50


            if context.transitions is None:
                context.transitions = self.transition_manager

            context.transitions.start_flash(post_flash_action=after_flash)

    def push_powerup_collision(self, context):
        for powerup in context.actors.powerups["powerups"]:
            if context.player.colliderect(powerup) and 'push_powerup' in powerup.image:
                if self.transition_manager:
                    self.transition_manager.show_powerup_message("Push logs with the space bar!", powerup._surf)
                context.sounds.p_powerup.play()
                context.actors.push_powerup_active = True
                powerup.pos = (random.choice(self.config["default_positions"]), randint(-2000, -1600))

                for log in context.actors.logs:
                    if hasattr(log, 'is_being_pushed'):
                        if not hasattr(log, 'original_pos'):
                            log.original_pos = (log.x, log.y)

                context.clock.start_timer('push_powerup', 5, context.actors.deactivate_push_powerup)


    def swimmer_cap_collision(self, context):
        if context.player.colliderect(context.actors.collectibles['swimmer_cap']):
            context.sounds.whip_1.play()
            context.clock.shield += 1 if context.clock.shield < 3 else 0
            context.actors.collectibles['swimmer_cap'].pos = randint(175, 625), randint(context.actors.collectibles['swimmer_cap'].first, context.actors.collectibles['swimmer_cap'].last)

    def magnet_collision(self, context):
        for magnet in context.actors.powerups["powerups"]:
            if "magnet" in magnet.image and context.player.colliderect(magnet):
                context.sounds.magnetic.set_volume(0.3)
                context.sounds.magnetic.play()
                context.actors.magnet_powerup_active = True
                magnet.pos = (random.choice(self.config["default_positions"]), randint(-2000, -1600))
                if self.transition_manager:
                    self.transition_manager.show_powerup_message("Attract objects!", magnet._surf)

                def deactivate_magnet():
                    context.actors.magnet_powerup_active = False

                context.clock.start_timer('magnet_powerup', 5, deactivate_magnet)

    def handle_bird_attack_collisions(self, context):
        # Egg collisions
        for egg in context.actors.bird_attack["eggs"]:
            if context.actors.swimmer.colliderect(egg):
                if context.clock.shield > 0:
                    context.clock.shield -= 1
                    context.sounds.shield_hit.play()
                else:
                    self.collision_penalty(context, speed_penalty=0.5, points_penalty=1)
                    context.sounds.sticky.play()
                egg.pos = (-1000, -1000)  # Remove egg
                break  # Only process one collision per frame

        # Debris collisions
        for debris in context.actors.bird_attack["egg_debris"]:
            if context.actors.swimmer.colliderect(debris):
                if context.clock.shield > 0:
                    context.clock.shield -= 1
                    context.sounds.shield_hit.play()
                else:
                    self.collision_penalty(context, speed_penalty=1, points_penalty=1)
                    context.sounds.sticky.play()
                debris.pos = (-1000, -1000)  # Remove debris
                break

