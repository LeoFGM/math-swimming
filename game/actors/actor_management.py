import random
from random import randint

from .actor_movement_interactions import  ActorMovementManager
from game.settings import settings
from game.actors.actor_factory import ActorStorage

HIDDEN_POSITION = (-500, -500)


class GameActors:
    def __init__(self):
        self.actor_storage = ActorStorage()
        self.actors = self.actor_storage.get_actors()
        self.actor_states = self.actor_storage.get_actor_states()

        self.start = self.actors["menu_actors"]["start"]
        self.speedrun = self.actors["menu_actors"]["speedrun"]
        self.pointsmania = self.actors["menu_actors"]["pointsmania"]
        self.gamename = self.actors["menu_actors"]["gamename"]
        self.gamemode = self.actors["menu_actors"]["gamemode"]
        self.goback = self.actors["menu_actors"]["goback"]
        self.difficulty = self.actors["difficulty_actors"]["difficulty"]
        self.easy = self.actors["difficulty_actors"]["easy"]
        self.medium = self.actors["difficulty_actors"]["medium"]
        self.hard = self.actors["difficulty_actors"]["hard"]
        self.extreme = self.actors["difficulty_actors"]["extreme"]
        self.swimmer = self.actors["game_actors"]["swimmer"]
        self.q_block = self.actors["game_actors"]["q_block"]
        self.shark = self.actors["game_actors"]["shark"]
        self.bear = self.actors["game_actors"]["bear"]
        self.poop = self.actors["game_actors"]["poop"]
        self.glasses = self.actors["game_actors"]["glasses"]
        self.inversion_portal = self.actors["game_actors"]["inversion_portal"]
        self.coins = []
        self.logs = []
        self.powerups = []
        self.powerup_collision = False
        self.push_powerup_active = False

        self.static_actors = [
            (self.gamename, self.actor_states["menu_states"]["gamename_states"], 15, 0),
            (self.gamemode, self.actor_states["menu_states"]["gamemode_states"], 15, 0),
            (self.difficulty, self.actor_states["difficulty_states"]["difficulty_states"], 5, 60),
            (self.easy, self.actor_states["difficulty_states"]["easy_states"], 5, 60),
            (self.medium, self.actor_states["difficulty_states"]["medium_states"], 5, 60),
            (self.hard, self.actor_states["difficulty_states"]["hard_states"], 5, 60),
            (self.extreme, self.actor_states["difficulty_states"]["extreme_states"], 5, 60)
        ]

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
            "glasses": self.glasses,
            "inversion_portal": self.inversion_portal
        }

    def get_moving_actors_states(self):
        return self.actor_states

    def stop_powerup(self, game_clocks):
        self.powerup_collision = False
        for powerup in self.powerups:
            if 'speed' in powerup.image:
                game_clocks.stop_timer('speed_powerup')
            elif 'score' in powerup.image:
                game_clocks.stop_timer('score_powerup')

    def deactivate_push_powerup(self, game_clocks):
        print("Deactivating push_powerup")
        self.push_powerup_active = False
        print(self.push_powerup_active)
        game_clocks.stop_timer('push_powerup')
        self.reset_pushed_logs()

    def reset_pushed_logs(self):
        for log in self.logs:
            if hasattr(log, 'is_being_pushed'):
                # Get original lane if available, otherwise assign random
                if hasattr(log, 'original_pos'):
                    x_pos = log.original_pos[0]  # Keep original x position
                else:
                    x_pos = random.choice(ActorMovementManager.DEFAULT_POSITIONS)

                log.pos = (x_pos, randint(-800, -500))

                # Clean up push state
                for attr in ['is_being_pushed', 'push_start_time', 'original_pos']:
                    if hasattr(log, attr):
                        delattr(log, attr)


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
        self.push_powerup_active = False

    def set_actor_position(self, actor, position):
        actor.pos = position

    def hide_level_selection_actors(self):
        level_selection_actors = [self.start, self.gamename, self.gamemode, self.difficulty,
                                  self.pointsmania, self.speedrun, self.easy, self.medium,
                                  self.hard, self.extreme
        ]
        for actor in level_selection_actors:
            self.set_actor_position(actor, HIDDEN_POSITION)


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
        actor_mapping = {
            self.start: 'start',
            self.speedrun: 'speedrun',
            self.pointsmania: 'pointsmania',
            self.easy: 'easy',
            self.medium: 'medium',
            self.hard: 'hard',
            self.extreme: 'extreme',
            self.goback: 'goback',
        }
        for actor, return_value in actor_mapping.items():
            if actor.collidepoint(pos):
                return return_value
        return None