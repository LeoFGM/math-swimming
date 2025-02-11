import random
from random import randint

from pgzero.actor import Actor
from pgzero.keyboard import keyboard

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
        self.coins = []
        self.logs = []
        self.powerups = []
        self.powerup_collision = False

        self.game_name_states = ["title", "title_2", "title_3", "title_4"]  # Main title images
        self.gamemode_states = ["selgamemode_1", "selgamemode_2", "selgamemode_3", "selgamemode_4"]  # Select gamemode images
        self.title_states_diff = ["selectdiff_1", "selectdiff_2", "selectdiff_3",
                             "selectdiff_4", "selectdiff"]  # Select difficulty images
        self.title_states_easy = ["easy_1", "easy_2", "easy_3", "easy_4", "easy"]  # Easy animation images
        self.title_states_medium = ["medium_1", "medium_2", "medium_3", "medium_4", "medium"]  # Medium animation images
        self.title_states_hard = ["hard_1", "hard_2", "hard_3", "hard_4", "hard"]  # Hard animation images
        self.title_states_extreme = ["extreme_1", "extreme_2", "extreme_3",
                                "extreme_4", "extreme"]  # Extreme animation images
        self.log_states = ["log", "log_1"]  # log animation images
        self.swimmer_states = ["swimmer", "swimmer_1", "swimmer_2", "swimmer_3"]  # swimmer not-hit animation images
        self.swimmer_states_hit = ["swimmer", "swimmer_hit", "swimmer_1", "swimmer_hit", "swimmer_2",
                              "swimmer_3"]  # swimmer hit animation images
        self.powerup_states = ["powerup", "powerup_1", "powerup_2"]  # powerup animation images
        self.coin_states = ["coin", "coin_1", "coin_2"]  # coin animation images
        self.shark_states = ["shark", "shark_1", "shark_2", "shark_3", "shark_4", "shark_5", "shark_6", "shark_7", "shark_8",
                        "shark_9", "shark_10", "shark_11", "shark_12", "shark_13", "shark_14"]
        self.q_block_states = ["question_block", "question_block_1"]

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

    def new_power_up(self):
        powerup = Actor("powerup")
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
            "coins": self.coins, "coins_states": self.coin_states,
            "logs": self.logs, "logs_states": self.log_states,
            "powerups": self.powerups, "powerups_states": self.powerup_states,
            "q_block": self.q_block, "q_block_states": self.q_block_states,
            "shark": self.shark, "shark_states": self.shark_states,
            "swimmer": self.swimmer, "swimmer_states": self.swimmer_states,
            "swimmer_states_hit": self.swimmer_states_hit,
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



class ActorMovement:
    def __init__(self):
        self.scroll = 0
        self.neg = 1
        self.backgrounds = []

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

    def actors_pos_x_fixated(self, actor, quantity, special_effect, quantity2, first, last):
        if actor.y < 600 and not special_effect:
            actor.y += quantity
        elif actor.y < 600 and special_effect:
            actor.y += quantity2
        else:
            actor.pos = random.choice([250, 400, 550]), randint(first, last)

    def actors_random_pos(self, actor, quantity, special_effect, quantity2, first, last):
        if actor.y < 600 and not special_effect:
            actor.y += quantity
        elif actor.y < 600 and special_effect:
            actor.y += quantity2
        else:
            actor.pos = randint(175, 625), randint(first, last)

class AnimationManager:
    def __init__(self, game_actors):
        self.game_actors = game_actors
        self.not_hit = True

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
        moving_actors = self.game_actors.get_moving_actors()
        for coin in moving_actors["coins"]:
            self.animate_actor(coin, moving_actors["coins_states"], update_interval=10)

        for log in moving_actors["logs"]:
            self.animate_actor(log, moving_actors["logs_states"], update_interval=10)

        for powerup in moving_actors["powerups"]:
            self.animate_actor(powerup, moving_actors["powerups_states"], update_interval=10)

        self.animate_actor(moving_actors["q_block"], moving_actors["q_block_states"], update_interval=15)
        self.animate_actor(moving_actors["shark"], moving_actors["shark_states"], update_interval=5, wait_time=60)

        if not self.not_hit:
            self.animate_actor(moving_actors["swimmer"], moving_actors["swimmer_states_hit"], update_interval=10)
        else:
            self.animate_actor(moving_actors["swimmer"], moving_actors["swimmer_states"], update_interval=10)

    def stop_swimmer_hit_animation(self):
        self.not_hit = True

    def static_update_animations(self):
        static_actors = self.game_actors.get_static_actors()
        for actor, states, update_interval, wait_time in static_actors:
            self.animate_actor(actor, states, update_interval, wait_time)











