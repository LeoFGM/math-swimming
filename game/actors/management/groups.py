import random
from random import randint

from game.actors.systems.movement.actor_movement import ActorMovementManager
from game.core.settings import settings
from game.actors.management.factory import ActorStorage

HIDDEN_POSITION = (-500, -500)

class ActorCategories:
    OBSTACLES = ['logs', 'shark', 'bear', 'poop']
    COLLECTIBLES = ['coins', 'glasses', 'swimmer_cap']
    POWERUPS = ['speed_powerup', 'score_powerup', 'push_powerup']
    SPECIAL = ['q_block', 'inversion_portal']
    ALL = OBSTACLES + COLLECTIBLES + POWERUPS + SPECIAL

class GameActors:
    def __init__(self, config=None):
        self.actor_storage = ActorStorage()
        self.actors = self.actor_storage.get_actors()
        self.actor_states = self.actor_storage.get_actor_states()
        self.config = config or {
            "default_positions": [250, 400, 550],
            "collision_cooldown": 3,
            "powerup_duration": 5,
        }

        self.swimmer = self.actors["game_actors"]["swimmer"]

        self.coins = []
        self.logs = []

        self.powerups = {
            "powerups": [],
            "speed_powerup": [],
            "score_powerup": [],
            "push_powerup": [],
            "magnet_powerup": [],
        }

        self.speed_powerup_collision = False
        self.score_powerup_collision = False
        self.push_powerup_active = False
        self.magnet_powerup_active = False

        self.obstacles = self._init_obstacles()
        self.collectibles = self._init_collectibles()
        self.powerups = self._init_powerups()
        self.special = self._init_special()
        self.menu = self._init_menu_actors()
        self.bird_attack = self._init_bird_attack()

        self.category_map = {
            'menu': self.menu,
            'obstacles': self.obstacles,
            'collectibles': self.collectibles,
            'powerups': self.powerups,
            'special': self.special,
            'bird_attack': self.bird_attack
        }

    def _init_menu_actors(self):
        self.menu = {
            "start": {"actor": self.actors["menu_actors"]["start"],
                      "states": self.actor_states["menu_states"]["start_states"],
                      "update_interval": 5, "wait_time": 60},
            "gamename": {"actor": self.actors["menu_actors"]["gamename"],
                         "states": self.actor_states["menu_states"]["gamename_states"],
                         "update_interval": 15, "wait_time": 0},
            "gamemode": {"actor": self.actors["menu_actors"]["gamemode"],
                         "states": self.actor_states["menu_states"]["gamemode_states"],
                         "update_interval": 15, "wait_time": 0},
            "speedrun": {"actor": self.actors["menu_actors"]["speedrun"],
                         "states": self.actor_states["menu_states"].get("speedrun_states", []),
                         "update_interval": 15, "wait_time": 0},
            "pointsmania": {"actor": self.actors["menu_actors"]["pointsmania"],
                            "states": self.actor_states["menu_states"].get("pointsmania_states", []),
                            "update_interval": 15, "wait_time": 0},
            "difficulty": {"actor": self.actors["difficulty_actors"]["difficulty"],
                           "states": self.actor_states["difficulty_states"]["difficulty_states"],
                           "update_interval": 5, "wait_time": 60},
            "easy": {"actor": self.actors["difficulty_actors"]["easy"],
                     "states": self.actor_states["difficulty_states"]["easy_states"],
                     "update_interval": 5, "wait_time": 60},
            "medium": {"actor": self.actors["difficulty_actors"]["medium"],
                       "states": self.actor_states["difficulty_states"]["medium_states"],
                       "update_interval": 5, "wait_time": 60},
            "hard": {"actor": self.actors["difficulty_actors"]["hard"],
                     "states": self.actor_states["difficulty_states"]["hard_states"],
                     "update_interval": 5, "wait_time": 60},
            "extreme": {"actor": self.actors["difficulty_actors"]["extreme"],
                        "states": self.actor_states["difficulty_states"]["extreme_states"],
                        "update_interval": 5, "wait_time": 60},
            "goback": {"actor": self.actors["menu_actors"]["goback"],
                       "states": ["goback"], "update_interval": 15, "wait_time": 0},
        }
        return self.menu

    def _init_obstacles(self):
        self.obstacles = {
            "logs": self.logs,
            "shark": self.actors["game_actors"]["shark"],
            "bear": self.actors["game_actors"]["bear"],
            "poop": self.actors["game_actors"]["poop"],

        }
        return self.obstacles

    def _init_powerups(self):
        self.powerups = {
            "powerups": self.powerups["powerups"],
            "speed_powerup": self.powerups["speed_powerup"],
            "score_powerup": self.powerups["score_powerup"],
            "push_powerup": self.powerups["push_powerup"],
            "magnet_powerup": self.powerups["magnet_powerup"]
        }
        return self.powerups


    def _init_collectibles(self):
        self.collectibles = {
            "coins": self.coins,
            "glasses": self.actors["game_actors"]["glasses"],
            "swimmer_cap": self.actors["game_actors"]["swimmer_cap"]
        }
        return self.collectibles

    def _init_special(self):
        self.special = {
            "q_block": self.actors["game_actors"]["q_block"],
            "inversion_portal": self.actors["game_actors"]["inversion_portal"]
        }
        return self.special

    def _init_bird_attack(self):
        self.bird_attack = {
            "birds": [],
            "eggs": [],
            "egg_debris": []
        }
        return  self.bird_attack

    def get_actors_by_category(self, category_name, *specific_actors):
        category = self.category_map.get(category_name, {})

        if not specific_actors:
            return [actor for actor in category.values() if not isinstance(actor, list)] + \
                [item for sublist in category.values() if isinstance(sublist, list) for item in sublist]

        result = []
        for actor_name in specific_actors:
            actor = category.get(actor_name)
            if isinstance(actor, list):
                result.extend(actor)
            elif actor:
                result.append(actor)
        return result

    def draw_category(self, category_name, *specific_actors):
        category = self.category_map.get(category_name, {})

        actors_to_draw = []

        if specific_actors:
            for actor_name in specific_actors:
                actor_data = category.get(actor_name)
                if actor_data is None:
                    continue

                if isinstance(actor_data, dict) and 'actor' in actor_data:
                    actors_to_draw.append(actor_data['actor'])

                elif isinstance(actor_data, list):
                    actors_to_draw.extend(actor_data)

                else:
                    actors_to_draw.append(actor_data)
        else:
            for actor_data in category.values():
                if isinstance(actor_data, dict) and 'actor' in actor_data:
                    actors_to_draw.append(actor_data['actor'])
                elif isinstance(actor_data, list):
                    actors_to_draw.extend(actor_data)
                else:
                    actors_to_draw.append(actor_data)

        for actor in actors_to_draw:
            if hasattr(actor, 'draw'):
                actor.draw()
            else:
                print(f"Warning {actor} has no draw method")


    def deactivate_push_powerup(self):
        print("Deactivating push_powerup")
        self.push_powerup_active = False
        self.reset_pushed_logs()

    def reset_pushed_logs(self):
        for log in self.logs:
            if hasattr(log, 'is_being_pushed'):
                if hasattr(log, 'original_pos'):
                    x_pos = log.original_pos[0]
                else:
                    x_pos = random.choice(self.config["default_positions"])

                log.pos = (x_pos, randint(-800, -500))

                for attr in ['is_being_pushed', 'push_start_time', 'original_pos']:
                    if hasattr(log, attr):
                        delattr(log, attr)


    def reset_all_actors(self):
        self.logs.clear()
        self.coins.clear()
        self.powerups["powerups"].clear()
        self.powerups["speed_powerup"].clear()
        self.powerups["score_powerup"].clear()
        self.powerups["push_powerup"].clear()
        self.push_powerup_active = False

    @staticmethod
    def set_actor_position(actor, position):
        actor.pos = position

    def hide_level_selection_actors(self):
        for key, menu_item in self.menu.items():
            if key == "goback":
                continue
            actor = menu_item["actor"]
            actor.original_pos = actor.pos
            self.set_actor_position(actor, HIDDEN_POSITION)


    def show_level_selection_actors(self):
        for key, menu_item in self.menu.items():
            if key == "goback":
                continue
            actor = menu_item['actor']
            if hasattr(actor, 'original_pos'):
                self.set_actor_position(actor, actor.original_pos)

    def handle_mouse_down(self, pos):
        actor_mapping = {
            self.menu["start"]["actor"]: 'start',
            self.menu["speedrun"]["actor"]: 'speedrun',
            self.menu["pointsmania"]["actor"]: 'pointsmania',
            self.menu["easy"]["actor"]: 'easy',
            self.menu["medium"]["actor"]: 'medium',
            self.menu["hard"]["actor"]: 'hard',
            self.menu["extreme"]["actor"]: 'extreme',
            self.menu["goback"]["actor"]: 'goback',
        }
        for actor, return_value in actor_mapping.items():
            if hasattr(actor, 'collidepoint') and actor.collidepoint(pos):
                return return_value
        return None