import random

from pgzero.actor import Actor
from random import randint
from game.core.settings import settings

HIDDEN_POSITION = (-500, -500)

class ActorStorage:
    def __init__(self):
        self.center_x = settings.CENTER_X
        self.actors = {
            "menu_actors": self.create_menu_actors(),
            "game_actors": self.create_game_actors(),
            "difficulty_actors": self.create_difficulty_actors(),
            "powerups": self.create_powerups(),
            "obstacles": self.create_obstacles(),
        }

        self.actor_states = {
            "menu_states": self.create_menu_states(),
            "game_states": self.create_game_states(),
            "difficulty_states": self.create_difficulty_states(),
            "powerup_states": self.create_powerup_states(),
            "obstacle_states": self.create_obstacle_states(),
        }

    def new_actor(self, image_name, position=None, actor_list=None, category=None, subcategory=None, special_x=None, x_locked=False, x_positions=None, first=None, last=None):
        if position is None:
            position = (self.center_x, 0)

        actor = Actor(image_name, pos=position)
        actor.current_frame = 0
        actor.frame_counter = 0
        actor.waiting_time = 0
        actor.use_random_choice = False
        actor.x_positions = None

        if actor_list is not None:
            if isinstance(actor_list, list):
                actor_list.append(actor)
            elif isinstance(actor_list, dict):
                actor_list[image_name] = actor

        elif category is not None:
            if category not in self.actors:
                self.actors[category] = {}
            if subcategory:
                if subcategory not in self.actors[category]:
                    self.actors[category][subcategory] = []
                self.actors[category][subcategory].append(actor)
            else:
                self.actors[category][image_name] = actor

        if special_x is not None:
            actor.x = special_x

        if x_locked:
            actor.use_random_choice = True
            actor.x_positions = x_positions

        actor.first = first
        actor.last = last

        return actor

    def create_menu_actors(self):
        return {
            "start": self.new_actor("start", (self.center_x, 550)),
            "speedrun": self.new_actor("speedrun", (self.center_x - 200, 450)),
            "pointsmania": self.new_actor("pointsmania", (self.center_x + 200, 450)),
            "gamename": self.new_actor("title", (self.center_x, 250)),
            "gamemode": self.new_actor("selgamemode_1", (self.center_x, 250)),
            "goback": self.new_actor("goback", (50, 580)),
        }

    def create_game_actors(self):
        return {
            "swimmer": self.new_actor("swimmer", (self.center_x, 550)),
            "q_block": self.new_actor("question_block", (self.center_x, randint(-2000, -1600)), x_locked=True, first=-2000, last=-1600),
            "shark": self.new_actor("shark", (randint(250, 550), randint(-800, -400)), x_locked=True, first=-800, last=-400),
            "bear": self.new_actor("bear", (random.choice([110, 700]), randint(-1000, -800)), x_locked=True, x_positions=[110, 700], first=-1000, last=-800),
            "poop": self.new_actor("poop", (random.choice([110, 700]), randint(-1000, -800)), first=-5000, last=-4900),
            "glasses": self.new_actor("glasses", (random.choice([250, 550]), randint(-1000, -800)), x_locked=True, first=-1000, last=-800),
            "inversion_portal": self.new_actor("inversion_portal", (random.choice([250, 400, 550]), randint(-3000, -2500)), x_locked=True, first=-3000, last=-2500),
            "swimmer_cap": self.new_actor("swimmer_cap", position=(random.choice([250, 400, 550]), randint(-2500, -1200)), x_locked=True, first=-2500, last=-1200)

        }

    def create_difficulty_actors(self):
        return {
            "difficulty": self.new_actor("selectdiff", (self.center_x, 175)),
            "easy": self.new_actor("easy", (self.center_x - 200, 350)),
            "medium": self.new_actor("medium", (self.center_x + 200, 350)),
            "hard": self.new_actor("hard", (self.center_x - 200, 525)),
            "extreme": self.new_actor("extreme", (self.center_x + 200, 525)),
        }

    def create_powerups(self):
        return {
            "speed_powerup": self.new_actor("speed_powerup", HIDDEN_POSITION),
            "score_powerup": self.new_actor("score_powerup", HIDDEN_POSITION),

        }

    def create_obstacles(self):
        return {
            "log": self.new_actor("log", HIDDEN_POSITION),
            "coin": self.new_actor("coin", HIDDEN_POSITION),
            "bird": self.new_actor("bird", HIDDEN_POSITION),
            "egg": self.new_actor("egg", HIDDEN_POSITION)
        }

    def create_menu_states(self):
        return {
            "start_states": ["start", "start_1", "start_2", "start_3", "start_4", "start_5", "start"],
            "gamename_states": ["title", "title_2", "title_3", "title_4"],
            "gamemode_states": ["selgamemode_1", "selgamemode_2", "selgamemode_3", "selgamemode_4"],
        }

    def create_game_states(self):
        return {
            "swimmer_states": ["swimmer", "swimmer_1", "swimmer_2", "swimmer_3"],
            "swimmer_states_hit": ["swimmer", "swimmer_hit", "swimmer_1", "swimmer_hit", "swimmer_2", "swimmer_3"],
            "shark_states": ["shark", "shark_1", "shark_2", "shark_3", "shark_4", "shark_5", "shark_6", "shark_7", "shark_8", "shark_9", "shark_10", "shark_11", "shark_12", "shark_13", "shark_14"],
            "bear_states": ["bear", "bear_1"],
            "poop_states": ["poop", "poop_1", "poop_2"],
            "glasses_states": ["glasses", "glasses_1", "glasses_2", "glasses_3", "glasses_4", "glasses"],
            "q_block_states": ["question_block", "question_block_1"],
            "swimmer_inv_states": ["swimmer_inv", "swimmer_inv_1", "swimmer_inv_2", "swimmer_inv_3"],
            "swimmer_inv_hit_states": ["swimmer_inv", "swimmer_hit", "swimmer_inv_1", "swimmer_hit", "swimmer_inv_2", "swimmer_inv_3"],
            "shark_inv_states": ["shark_inv", "shark_inv_1", "shark_inv_2", "shark_inv_3", "shark_inv_4", "shark_inv_5", "shark_inv_6", "shark_inv_7", "shark_inv_8", "shark_inv_9", "shark_inv_10", "shark_inv_11", "shark_inv_12", "shark_inv_13"],
            "bear_inv_states": ["bear_inv", "bear_inv_1"],
            "poop_inv_states": ["poop_inv", "poop_inv_1", "poop_inv_2"],
            "swimmer_push_states": ["swimmer_push", "swimmer_push_1", "swimmer_push_2", "swimmer_push_3"],
            "swimmer_push_hit_states": ["swimmer_push", "swimmer_hit", "swimmer_push_1", "swimmer_hit", "swimmer_push_2", "swimmer_push_3"],
            "swimmer_cap_states":["swimmer_cap", "swimmer_cap_1", "swimmer_cap_2", "swimmer_cap_1"],
            "bird_states": ["bird", "bird_1"],
            "egg_states": ["egg", "egg_cracking"],
            "egg_debris_states": ["egg_shell", "egg_cracked"]
        }


    def create_difficulty_states(self):
        return {
            "difficulty_states": ["selectdiff_1", "selectdiff_2", "selectdiff_3", "selectdiff_4", "selectdiff"],
            "easy_states": ["easy_1", "easy_2", "easy_3", "easy_4", "easy"],
            "medium_states": ["medium_1", "medium_2", "medium_3", "medium_4", "medium"],
            "hard_states": ["hard_1", "hard_2", "hard_3", "hard_4", "hard"],
            "extreme_states": ["extreme_1", "extreme_2", "extreme_3", "extreme_4", "extreme"],
        }

    def create_powerup_states(self):
        return {
            "speed_powerup_states": ["speed_powerup", "speed_powerup_1", "speed_powerup_2"],
            "score_powerup_states": ["score_powerup", "score_powerup_1", "score_powerup_2", "score_powerup_3", "score_powerup_4", "score_powerup_5", "score_powerup_6", "score_powerup_7", "score_powerup_8", "score_powerup_9", "score_powerup_10", "score_powerup_11"],
            "push_powerup_states": ["push_powerup", "push_powerup_1"],
            "magnet_powerup_states": ["magnet_powerup", "magnet_powerup_1", "magnet_powerup_2"]
        }

    def create_obstacle_states(self):
        return {
            "log_states": ["log", "log_1"],
            "coin_states": ["coin", "coin_1", "coin_2"],
            "log_inv_states": ["log_inv", "log_inv_1"]
        }

    def get_actors(self):
        return self.actors

    def get_actor_states(self):
        return self.actor_states