import random
import threading
import time
from random import randint
from pgzero import clock
from pgzero.loaders import sounds
from pgzero.animation import animate

class CompActors:
    def __init__(self, game_actors, transition_manager=None):
        self.game_actors = game_actors
        self.transition_manager = transition_manager
        self.bear = game_actors.obstacles["bear"]
        self.bear_states = game_actors.actor_states["game_states"]["bear_states"]
        self.poop = game_actors.obstacles["poop"]
        self.poop_states = game_actors.actor_states["game_states"]["poop_states"]
        self.pooping_pos = randint(200, 400)
        self.poop_pos = "not_pooping"

        #Bird attack content
        self.bird_attack_active = False
        self.bird_attack_start_time = 0
        self.bird_attack_duration = 8.0
        self.bird_attack_spawn_chance = 0.00005

    def pooping(self, context):
        if self.bear.waiting_time > 0:
            self.bear.waiting_time -= 1
            return

        if self.bear.y == self.pooping_pos:
            self.bear.waiting_time = 30
            if self.bear.x == 110:
                self.bear.image = "bear_inv_poop_right" if context.animation.inversion_active else "bear_poop_right"
                self.poop.pos = self.bear.x + 140, self.bear.y
            elif self.bear.x == 700:
                self.bear.image = "bear_inv_poop_left" if context.animation.inversion_active else "bear_poop_left"
                self.poop.pos = self.bear.x - 150, self.bear.y
            self.poop_pos = "pooping_time"

    def bear_actions(self, context):
        if self.bear.waiting_time > 0:
            if self.bear.waiting_time == 30:
                sounds.fart.set_volume(0.4)
                sounds.fart.play()
            elif self.bear.waiting_time == 10:
                sounds.water_splash.set_volume(0.2)
                sounds.water_splash.play()
        else:
            # Movement direction based on inversion
            move_amount = -1 if context.animation.inversion_active else 1
            self.bear.y += move_amount

            # Repositioning logic
            if context.animation.inversion_active:
                if self.bear.y < -1000:
                    self.bear.y = 630
                    self.bear.x = random.choice([110, 700])  # Bear's fixed X positions
                    self.pooping_pos = randint(200, 400)  # Reset pooping position
            else:
                # Normal mode - when bear moves below screen (y > 630)
                if self.bear.y > 630:
                    # Reset to top with random Y in initial range
                    self.bear.y = randint(self.bear.first, self.bear.last)
                    self.pooping_pos = randint(200, 400)  # Reset pooping position

        # Poop handling
        if 630 > self.poop.y > 0:
            if "poop" in self.bear.image:
                poop_speed = 0.5 * (-1 if context.animation.inversion_active else 1)
            else:
                poop_speed = 2.5 * (-1 if context.animation.inversion_active else 1)
            self.poop.y += poop_speed
        else:
            self.poop_pos = "not_pooping"
            self.poop.y = -5000

    def start_bird_attack(self):
        if self.bird_attack_active:
            return

        def starting():
            sounds.bird_attack.play()
            time.sleep(1.5)
            self.bird_attack_active = True

        self.bird_attack_start_time = time.time()

        for i in range(8):
            bird = self.game_actors.actor_storage.new_actor("bird", position=(randint(100, 700), -100 - (i * 100)), first=-200, last=-800)
            bird.attack_path = self._generate_parabolic_path(bird.x)
            bird.path_index = 0
            self.game_actors.bird_attack["birds"].append(bird)

        if self.transition_manager:
            try:
                bird_icon = self.game_actors.bird_attack["birds"][0]._surf
                self.transition_manager.show_powerup_message(
                    "BIRD ATTACK!",
                    bird_icon
                )
            except:
                print("Could not load bird attack icon")

        threading.Thread(target=starting).start()

    def _generate_parabolic_path(self, start_x):
        end_x = randint(100, 700)
        peak_height = randint(150, 300)
        steps = 100
        path = []

        for i in range(steps + 1):
            t = i / steps
            x = start_x + (end_x - start_x) * t
            y = -100 + (peak_height * 4 * t * (1 - t))
            path.append((x, y))
        return path

    def update_bird_attack(self, dt):
        if not self.bird_attack_active:
            if random.random() < self.bird_attack_spawn_chance:
                self.start_bird_attack()
            return

        current_time = time.time()
        elapsed = current_time - self.bird_attack_start_time
        print(f"Bird attack elapsed: {elapsed}/{self.bird_attack_duration}")  # Debug

        if elapsed + 0.1 >= self.bird_attack_duration:
            print("Attempting to end bird attack")  # Debug
            self._end_bird_attack()
            return

        for bird in self.game_actors.bird_attack["birds"]:
            if bird.path_index < len(bird.attack_path):
                bird.x, bird.y = bird.attack_path[bird.path_index]
                bird.path_index += 1

                if (random.random() < 0.02 and
                        bird.path_index > 25 and
                        240 <= bird.x <= 575):
                    self._drop_egg(bird.x, bird.y)

        for egg in self.game_actors.bird_attack["eggs"]:
            if not hasattr(egg, 'fall_speed'):
                egg.fall_speed = randint(3, 6)
                egg.wobble = random.random() * 2 - 1

            egg.y += egg.fall_speed * dt * 60
            egg.x += egg.wobble * dt * 60

            if egg.y > 400 and not hasattr(egg, 'cracked'):
                self._crack_egg(egg)

        for debris in self.game_actors.bird_attack["egg_debris"]:
            debris.y += 1 * dt * 60
            debris.x += debris.wobble * dt * 60

    def _drop_egg(self, x, y):
        egg = self.game_actors.actor_storage.new_actor(
            "egg", position=(x, y), actor_list=self.game_actors.bird_attack["eggs"], first=-800, last=-600
        )
        egg.fall_speed = randint(3, 6)
        egg.wobble = random.random() * 2 - 1

    def _crack_egg(self, egg):
        egg.image = "egg_cracked"
        egg.cracked = True

        self.game_actors.egg_debris = self.game_actors.bird_attack["egg_debris"]

        for i in range(2):
            shell = self.game_actors.actor_storage.new_actor("egg_shell", position=(egg.x + random.randint(-10, 10), egg.y + random.randint(-5, 5)),
                                                             actor_list=self.game_actors.egg_debris)
            shell.wobble = random.random() * 0.5 - 0.25

        yolk = self.game_actors.actor_storage.new_actor("egg_yolk", position=(egg.x, egg.y), actor_list=self.game_actors.egg_debris)
        yolk.wobble = random.random() * 0.3 - 0.15

        clock.schedule(lambda: self.game_actors.eggs.remove(egg), 2.0)

    def _end_bird_attack(self):
        self.bird_attack_active = False
        print(f"Bird attack ended! {self.bird_attack_active}")
        animate(self.game_actors.swimmer, tween='linear', duration=1, pos=(400, 550))
        self.game_actors.bird_attack["birds"] = []
        self.game_actors.bird_attack["eggs"] = []
        self.game_actors.bird_attack["egg_debris"] = []