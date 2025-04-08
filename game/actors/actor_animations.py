import time
from pgzero.clock import clock
from pygame import transform
from pgzero.loaders import sounds

from game.settings import settings


class AnimationManager:
    def __init__(self, game_actors):
        self.game_actors = game_actors
        self.not_hit = True
        self.moving_actors = self.game_actors.get_moving_actors()
        self.moving_actors_states = self.game_actors.get_moving_actors_states()

        self.inverted_actors = {}  # Stores original image names
        self.inversion_active = False
        self.inversion_end_time = 0

        self.background_manager = None

    def set_background_manager(self, background_manager):
        self.background_manager = background_manager

    def get_all_actors(self):
        actors = []

        actors.extend([
            self.moving_actors["swimmer"],
            self.moving_actors["q_block"],
            self.moving_actors["shark"],
            self.moving_actors["bear"],
            self.moving_actors["poop"],
            self.moving_actors["glasses"],
            self.moving_actors["inversion_portal"]
        ])

        actors.extend(self.moving_actors["coins"])
        actors.extend(self.moving_actors["logs"])
        actors.extend(self.moving_actors["powerups"])

        return actors


    def activate_inversion(self, duration=10.0):
        if not self.inversion_active:
            self.inversion_active = True
            self.inversion_end_time = time.time() + duration

            for actor in self.get_all_actors():
                if hasattr(actor, '_surf') and actor._surf:
                    self.inverted_actors[actor] = actor._surf.copy()
                    actor._surf = transform.flip(actor._surf, False, True)

            clock.schedule_unique(self.deactivate_inversion, duration)

    def deactivate_inversion(self):
        if self.inversion_active:
            self.inversion_active = False
            sounds.inversion.play()
            for actor, original_surf in self.inverted_actors.items():
                if hasattr(actor, '_surf'):
                    actor._surf = original_surf

            clock.schedule_unique(self._complete_deactivation, 0.1)

    def _complete_deactivation(self):
        self.game_actors.q_block.x = settings.CENTER_X
        self.game_actors.swimmer.y = 550
        if self.background_manager:
            self.background_manager.is_inverted = False
        self.inverted_actors.clear()

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
                if self.inversion_active:
                    if self.inversion_active and hasattr(actor, '_surf') and actor._surf:
                        if actor not in self.inverted_actors:
                            self.inverted_actors[actor] = actor._surf.copy()
                        actor._surf = transform.flip(actor._surf, False, True)
            else:
                print(f"Error: actor.current_frame ({actor.current_frame}) está fuera del rango de states (tamaño {len(states)}).")
                actor.current_frame = 0
            actor.current_frame = (actor.current_frame + 1) % len(states) if states else 0
            actor.frame_counter = 0
            if actor.current_frame == 0:
                actor.waiting_time = wait_time

    def moving_update_animations(self):
        for coin in self.moving_actors["coins"]:
            self.animate_actor(coin, self.moving_actors_states["obstacle_states"]["coin_states"], update_interval=10)

        for powerup in self.moving_actors["powerups"]:
            if "score" in powerup.image:
                self.animate_actor(powerup, self.moving_actors_states["powerup_states"]["score_powerup_states"], update_interval=3, wait_time=10)
            elif "speed" in powerup.image:
                self.animate_actor(powerup, self.moving_actors_states["powerup_states"]["speed_powerup_states"], update_interval=10)
            if "push" in powerup.image:
                self.animate_actor(powerup, self.moving_actors_states["powerup_states"]["push_powerup_states"], update_interval=30, wait_time=15)

        self.animate_actor(self.moving_actors["q_block"], self.moving_actors_states["game_states"]["q_block_states"], update_interval=15)
        self.animate_actor(self.moving_actors["glasses"], self.moving_actors_states["game_states"]["glasses_states"], update_interval=5, wait_time=30)
        self.moving_actors["inversion_portal"].angle += 3

        if not self.inversion_active:
            if not self.not_hit:
                if self.game_actors.push_powerup_active:
                    self.animate_actor(self.moving_actors["swimmer"], self.moving_actors_states["game_states"]["swimmer_push_hit_states"], update_interval=10)
                else:
                    self.animate_actor(self.moving_actors["swimmer"], self.moving_actors_states["game_states"]["swimmer_states_hit"], update_interval=10)
            else:
                if self.game_actors.push_powerup_active:
                    self.animate_actor(self.moving_actors["swimmer"], self.moving_actors_states["game_states"]["swimmer_push_states"], update_interval=10)
                else:
                    self.animate_actor(self.moving_actors["swimmer"], self.moving_actors_states["game_states"]["swimmer_states"], update_interval=10)
            self.animate_actor(self.moving_actors["poop"], self.moving_actors_states["game_states"]["poop_states"], update_interval=20, wait_time=30)
            self.animate_actor(self.moving_actors["shark"], self.moving_actors_states["game_states"]["shark_states"], update_interval=5, wait_time=60)
            for log in self.moving_actors["logs"]:
                self.animate_actor(log, self.moving_actors_states["obstacle_states"]["log_states"], update_interval=10)
            if self.moving_actors["bear"].waiting_time > 0:
                pass
            else:
                self.animate_actor(self.moving_actors["bear"], self.moving_actors_states["game_states"]["bear_states"], update_interval=10)

        elif self.inversion_active:
            if not self.not_hit:
                self.animate_actor(self.moving_actors["swimmer"],
                                   self.moving_actors_states["game_states"]["swimmer_inv_hit_states"], update_interval=10)
            else:
                self.animate_actor(self.moving_actors["swimmer"],
                                   self.moving_actors_states["game_states"]["swimmer_inv_states"], update_interval=10)
            self.animate_actor(self.moving_actors["poop"], self.moving_actors_states["game_states"]["poop_inv_states"], update_interval=20, wait_time=30)
            self.animate_actor(self.moving_actors["shark"], self.moving_actors_states["game_states"]["shark_inv_states"], update_interval=5, wait_time=60)
            for log in self.moving_actors["logs"]:
                self.animate_actor(log, self.moving_actors_states["obstacle_states"]["log_inv_states"], update_interval=10)
            if self.moving_actors["bear"].waiting_time > 0:
                pass
            else:
                self.animate_actor(self.moving_actors["bear"], self.moving_actors_states["game_states"]["bear_inv_states"], update_interval=10)




    def stop_swimmer_hit_animation(self):
        self.not_hit = True

    def static_update_animations(self):
        static_actors = self.game_actors.get_static_actors()
        for actor, states, update_interval, wait_time in static_actors:
            self.animate_actor(actor, states, update_interval, wait_time)
