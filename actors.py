import random
from random import randint

from pgzero.actor import Actor
from pgzero.keyboard import keyboard

from musicals import change_music_temporarily
from settings import settings


class GameActors:
    x = 250
    def __init__(self):
        self.start = self.new_actor("start", settings.CENTER_X, 550)
        self.speedrun = self.new_actor("speedrun", settings.CENTER_X - 200, 450)
        self.pointsmania = self.new_actor("pointsmania", settings.CENTER_X + 200, 450)
        self.gamename = self.new_actor("title", settings.CENTER_X, 250)
        self.gamemode = self.new_actor("selgamemode_1", settings.CENTER_X, 250)
        self.difficulty = self.new_actor("selectdiff", settings.CENTER_X, 175)
        self.easy = self.new_actor("easy", settings.CENTER_X - 200, 350)
        self.medium = self.new_actor("medium", settings.CENTER_X + 200, 350)
        self.hard = self.new_actor("hard", settings.CENTER_X - 200, 525)
        self.extreme = self.new_actor("extreme", settings.CENTER_X + 200, 525)
        self.goback = Actor("goback", pos=(50, 580))
        self.q_block = self.new_actor("question_block", settings.CENTER_X, randint(-2000, -1600))
        self.shark = self.new_actor("shark", randint(190, 625), randint(-800, -400))
        self.swimmer = self.new_actor("swimmer", settings.CENTER_X, 550)
        self.bear = self.new_actor("bear", random.choice([110, 700]), randint(-1000, -800))
        self.poop = self.new_actor("poop", random.choice([110, 700]), randint(-1000, -800))
        self.coins = []
        self.logs = []
        self.powerups = []
        self.powerup_collision = False

        self.game_name_states = ["title", "title_2", "title_3", "title_4"]  # Main title images
        self.gamemode_states = ["selgamemode_1", "selgamemode_2", "selgamemode_3", "selgamemode_4"]  # Select gamemode images
        self.title_states_diff = ["selectdiff_1", "selectdiff_2", "selectdiff_3", "selectdiff_4", "selectdiff"]  # Select difficulty images
        self.title_states_easy = ["easy_1", "easy_2", "easy_3", "easy_4", "easy"]  # Easy animation images
        self.title_states_medium = ["medium_1", "medium_2", "medium_3", "medium_4", "medium"]  # Medium animation images
        self.title_states_hard = ["hard_1", "hard_2", "hard_3", "hard_4", "hard"]  # Hard animation images
        self.title_states_extreme = ["extreme_1", "extreme_2", "extreme_3", "extreme_4", "extreme"]  # Extreme animation images


        self.static_actors = [
            (self.gamename, self.game_name_states, 15, 0),
            (self.gamemode, self.gamemode_states, 15, 0),
            (self.difficulty, self.title_states_diff, 5, 60),
            (self.easy, self.title_states_easy, 5, 60),
            (self.medium, self.title_states_medium, 5, 60),
            (self.hard, self.title_states_hard, 5, 60),
            (self.extreme, self.title_states_extreme, 5, 60)
        ]

    def new_actor(self, image_name, x, y):
        actor = Actor(image_name, pos=(x, y))
        actor.current_frame = 0
        actor.frame_counter = 0
        actor.waiting_time = 0
        return actor

    def new_log(self):
        log = Actor("log")
        log.current_frame = 0
        log.frame_counter = 0
        log.pos = self.x, randint(-800, -500)
        log.waiting_time = 0
        self.logs.append(log)
        self.x += 150
        return log

    def new_coin(self):
        coin = Actor("coin")
        coin.current_frame = 0
        coin.frame_counter = 0
        coin.pos = randint(175, 625), randint(-800, -300)
        coin.waiting_time = 0
        self.coins.append(coin)
        return coin

    def new_power_up(self, image):
        powerup = Actor(image)
        powerup.pos = random.choice([250, 400, 550]), self.logs[randint(0, 2)].y + 125
        powerup.current_frame = 0
        powerup.frame_counter = 0
        powerup.waiting_time = 0
        self.powerups.append(powerup)
        return powerup

    def get_static_actors(self):
        return self.static_actors

    def get_moving_actors(self):
        return {
            "coins": self.coins,
            "logs": self.logs,
            "powerups": self.powerups,
            "q_block": self.q_block,
            "shark": self.shark,
            "swimmer": self.swimmer,
            "bear": self.bear,
            "poop": self.poop,
        }

    def get_moving_actors_states(self):
        return {
            "coins_states": ["coin", "coin_1", "coin_2"],
            "logs_states": ["log", "log_1"],
            "speed_powerups_states": ["speed_powerup", "speed_powerup_1", "speed_powerup_2"],
            "score_powerups_states": ["score_powerup", "score_powerup_1", "score_powerup_2", "score_powerup_3", "score_powerup_4", "score_powerup_5",
                                     "score_powerup_6", "score_powerup_7", "score_powerup_8", "score_powerup_9", "score_powerup_10",'score_powerup_11'] ,
            "q_block_states": ["question_block", "question_block_1"],
            "shark_states": ["shark", "shark_1", "shark_2", "shark_3", "shark_4", "shark_5", "shark_6", "shark_7",
                             "shark_8", "shark_9", "shark_10", "shark_11", "shark_12", "shark_13", "shark_14"],
            "swimmer_states": ["swimmer", "swimmer_1", "swimmer_2", "swimmer_3"],
            "swimmer_states_hit": ["swimmer", "swimmer_hit", "swimmer_1", "swimmer_hit", "swimmer_2", "swimmer_3"],
            "bear_states": ["bear", "bear_1"],
            "poop_states": ["poop", "poop_1"]
        }

    def stop_powerup(self):
        self.powerup_collision = False

    def create_and_draw_actors(self, *actor_groups):
        for group in actor_groups:
            for actor in group:
                actor.draw()

    def draw_actors(self, *actors):
        for actor in actors:
            actor.draw()

    def reset_all_actors(self):
        self.logs.clear()
        self.coins.clear()
        self.powerups.clear()

    def hide_level_selection_actors(self):
        self.start.pos = (-500, -500)
        self.gamename.pos = (-500, -500)
        self.gamemode.pos = (-500, -500)
        self.difficulty.pos = (-500, -500)
        self.speedrun.pos = (-500, -500)
        self.pointsmania.pos = (-500, -500)
        self.easy.pos = (-500, -500)
        self.medium.pos = (-500, -500)
        self.hard.pos = (-500, -500)
        self.extreme.pos = (-500, -500)


    def show_level_selection_actors(self):
        self.start.pos = (settings.CENTER_X, 550)
        self.gamename.pos = (settings.CENTER_X, 250)
        self.gamemode.pos = (settings.CENTER_X, 250)
        self.speedrun.pos = (settings.CENTER_X - 200, 450)
        self.pointsmania.pos = (settings.CENTER_X + 200, 450)
        self.difficulty.pos = (settings.CENTER_X, 175)
        self.easy.pos = (settings.CENTER_X - 200, 350)
        self.medium.pos = (settings.CENTER_X + 200, 350)
        self.hard.pos = (settings.CENTER_X - 200, 525)
        self.extreme.pos = (settings.CENTER_X + 200, 525)

    def handle_mouse_down(self, pos):
        if self.start.collidepoint(pos):
            return 'start'
        elif self.speedrun.collidepoint(pos):
            return 'speedrun'
        elif self.pointsmania.collidepoint(pos):
            return 'pointsmania'
        elif self.easy.collidepoint(pos):
            return 'easy'
        elif self.medium.collidepoint(pos):
            return 'medium'
        elif self.hard.collidepoint(pos):
            return 'hard'
        elif self.extreme.collidepoint(pos):
            return 'extreme'
        elif self.goback.collidepoint(pos):
            return 'goback'
        return None



class ActorMovementInteractions:
    def __init__(self, actor_animation):
        self.actor_animation = actor_animation
        self.scroll = 0
        self.neg = 1
        self.backgrounds = []
        self.last_collision = 0

    def set_background(self,screen):
        screen.clear()
        for i in range(0, 3):
            bg = screen.blit("river", (0, i * (600 * self.neg) + self.scroll))
            self.backgrounds.append(bg)
            self.neg = -1

    def moving_bg(self):
        for back in self.backgrounds:
            self.scroll += 0.0003
        if abs(self.scroll) > 600:
            self.scroll = 0

    def moving(self, actor, objects, quantity, quantity2):
        if keyboard.left and (actor.x > 190):
            actor.x -= quantity
        if keyboard.right and (actor.x < 625):
            actor.x += quantity
        if keyboard.left and (actor.x > 190) and objects:
            actor.x -= quantity2
        if keyboard.right and (actor.x < 625) and objects:
            actor.x += quantity2

    def actors_pos_x_fixated(self, actor, quantity, special_effect, quantity2, first, last, a=250, b=400, c=550):
        if actor.y < 630 and not special_effect:
            actor.y += quantity
        elif actor.y < 630 and special_effect:
            actor.y += quantity2
        else:
            actor.pos = random.choice([a, b, c]), randint(first, last)

    def actors_random_pos(self, actor, quantity, special_effect, quantity2, first, last):
        if actor.y < 630 and not special_effect:
            actor.y += quantity
        elif actor.y < 630 and special_effect:
            actor.y += quantity2
        else:
            actor.pos = randint(175, 625), randint(first, last)

    def handle_all_collisions(self, excluded_actor):
        def process_actors():
            valid_actors = {}
            for name, actor in self.actor_animation.moving_actors.items():
                if isinstance(actor, list):
                    for i, item in enumerate(actor):
                        valid_actors[f"{name}_{i}"] = item
                else:
                    valid_actors[name] = actor
            return valid_actors

        valid_actors = process_actors()

        for name1, actor1 in valid_actors.items():
            if name1 != excluded_actor:
                for name2, actor2 in valid_actors.items():
                    if (name1 != name2) and (name1 != excluded_actor or name2 != excluded_actor) and (actor1.colliderect(actor2)):
                        self.collision_action(name1, actor1, name2, actor2)


    def collision_action(self, name1, actor1, name2, actor2):
        if ("coin" in name1 or "poop" in name1 or "shark" in name1 or "powerup" in name1) and ("log" in name2):
            actor1.y += 50
        elif ("log" in name1) and ("coin" in name2 or "poop" in name2 or "shark" in name2 or "powerup" in name2):
            actor2.y += 50
        elif ("q_block" in name1) and ("swimmer" != name2):
            actor2.y += 50
        elif ("swimmer" != name1) and ("q_block" in name2):
            actor1.y += 50

    def q_block_collision(self, current_screen, game_actors, game_questions, q_screen):
        if game_actors.swimmer.colliderect(game_actors.q_block):
            game_actors.q_block.y = randint(-2000, -1600)
            current_screen = 'question_time'
            game_questions.question_screen = q_screen
        return current_screen

    def log_collision(self, actor_animation, game_actors, game_clocks, log, sounds, ts):
        if (game_actors.swimmer.colliderect(log)) and (ts - self.last_collision >= 3):
            game_clocks.count_max += 3
            game_clocks.score -= 3
            self.last_collision = ts
            sounds.hit.play()
            actor_animation.not_hit = False

    def speed_powerup_collision(self, game_actors, game_clocks, powerup, new_music, duration, initial_music, clock):
        if game_actors.swimmer.colliderect(powerup):
            game_actors.powerup_collision = True
            game_clocks.count_max -= 5
            clock.schedule(game_actors.stop_powerup, 5)
            game_clocks.start_timer()
            powerup.pos = random.choice([250, 400, 550]), randint(-2000, -1600)
            change_music_temporarily(new_music, duration, initial_music)

    def score_powerup_collision(self, game_actors, game_clocks, powerup, sounds, clock):
        if game_actors.swimmer.colliderect(powerup):
            sounds.score_powerup.set_volume(0.5)
            sounds.score_powerup.play()
            game_actors.powerup_collision = True
            powerup.pos = random.choice([250, 400, 550]), randint(-2000, -1600)
            clock.schedule_unique(game_actors.stop_powerup, 5.0)
            game_clocks.start_timer()

    def shark_collision(self, game_actors, game_clocks, sounds):
        if game_actors.shark.colliderect(game_actors.swimmer) and not game_actors.shark.image == "shark_14":
            game_clocks.count_max += 3
            sounds.sharkbite.set_volume(0.5)
            sounds.sharkbite.play()
            game_actors.shark.image = "shark_14"
            game_actors.shark.pos = random.choice([250, 400, 550]), randint(-800, -500)

    def poop_collision(self, game_actors, game_clocks, sounds):
        if game_actors.swimmer.colliderect(game_actors.poop):
            game_clocks.score -= 5
            sounds.hit.set_volume(0.5)
            sounds.hit.play()
            game_actors.poop.pos = -5000, -5000

class AnimationManager:
    def __init__(self, game_actors):
        self.game_actors = game_actors
        self.not_hit = True
        self.moving_actors = self.game_actors.get_moving_actors()
        self.moving_actors_states = self.game_actors.get_moving_actors_states()

    def animate_actor(self, actor, states, update_interval, wait_time=0):
        if not hasattr(actor, 'current_frame'):
            actor.current_frame = 0
            actor.frame_counter = 0
            actor.waiting_time = 0

        if actor.waiting_time > 0:
            actor.waiting_time -= 1
            return

        actor.frame_counter += 1
        if actor.frame_counter >= update_interval:
            if 0 <= actor.current_frame < len(states):
                actor.image = states[actor.current_frame]
            else:
                print(f"Error: actor.current_frame ({actor.current_frame}) está fuera del rango de states (tamaño {len(states)}).")
                actor.current_frame = 0
            actor.current_frame = (actor.current_frame + 1) % len(states) if states else 0
            actor.frame_counter = 0
            if actor.current_frame == 0:
                actor.waiting_time = wait_time

    def moving_update_animations(self):
        for coin in self.moving_actors["coins"]:
            self.animate_actor(coin, self.moving_actors_states["coins_states"], update_interval=10)

        for log in self.moving_actors["logs"]:
            self.animate_actor(log, self.moving_actors_states["logs_states"], update_interval=10)

        for powerup in self.moving_actors["powerups"]:
            if "score" in powerup.image:
                self.animate_actor(powerup, self.moving_actors_states["score_powerups_states"], update_interval=3, wait_time=10)
            elif "speed" in powerup.image:
                self.animate_actor(powerup, self.moving_actors_states["speed_powerups_states"], update_interval=10)

        self.animate_actor(self.moving_actors["q_block"], self.moving_actors_states["q_block_states"], update_interval=15)
        self.animate_actor(self.moving_actors["shark"], self.moving_actors_states["shark_states"], update_interval=5, wait_time=60)

        if self.moving_actors["bear"].waiting_time > 0:
            pass
        else:
            self.animate_actor(self.moving_actors["bear"], self.moving_actors_states["bear_states"], update_interval=10)

        self.animate_actor(self.moving_actors["poop"], self.moving_actors_states["poop_states"], update_interval=30)
        if not self.not_hit:
            self.animate_actor(self.moving_actors["swimmer"], self.moving_actors_states["swimmer_states_hit"], update_interval=10)
        else:
            self.animate_actor(self.moving_actors["swimmer"], self.moving_actors_states["swimmer_states"], update_interval=10)

    def stop_swimmer_hit_animation(self):
        self.not_hit = True

    def static_update_animations(self):
        static_actors = self.game_actors.get_static_actors()
        for actor, states, update_interval, wait_time in static_actors:
            self.animate_actor(actor, states, update_interval, wait_time)


class CompActors:
    def __init__(self, game_actors):
        self.bear = game_actors.bear
        self.bear_states = game_actors.get_moving_actors_states()["bear_states"]
        self.poop = game_actors.poop
        self.poop_states = game_actors.get_moving_actors_states()["poop_states"]
        self.pooping_pos = randint(200, 400)
        self.poop_pos = "not_pooping"

    def pooping(self):
        if self.bear.waiting_time > 0:
            self.bear.waiting_time -= 1
            return
        if self.bear.y == self.pooping_pos:
            self.bear.waiting_time = 30
            if self.bear.x == 110:
                self.bear.image = "bear_poop_right"
                self.poop.pos = self.bear.x + 140, self.bear.y
            elif self.bear.x == 700:
                self.bear.image = "bear_poop_left"
                self.poop.pos = self.bear.x - 150, self.bear.y
            self.poop_pos = "pooping_time"

















