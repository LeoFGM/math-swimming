import time
from pgzero import clock
from pygame import transform
from pgzero.loaders import sounds

from game.core.settings import settings


class AnimationManager:
    def __init__(self, game_actors):
        self.game_actors = game_actors
        self.not_hit = True
        self.moving_actors_states = self.game_actors.actor_states

        self.inverted_actors = {}
        self.inversion_active = False
        self.inversion_end_time = 0

        self.background_manager = None

    def set_background_manager(self, background_manager):
        self.background_manager = background_manager


    def activate_inversion(self, duration=10.0):
        if not self.inversion_active:
            self.inversion_active = True
            self.inversion_end_time = time.time() + duration

            categories_to_invert = ['obstacles', 'collectibles', 'special', 'powerups']
            actors_to_invert = []

            for category in categories_to_invert:
                category_actors = self.game_actors.category_map.get(category, {})
                for actor_or_list in category_actors.values():
                    if isinstance(actor_or_list, list):
                        actors_to_invert.extend(actor_or_list)
                    else:
                        actors_to_invert.append(actor_or_list)

            for actor in actors_to_invert:
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
        self.game_actors.special['q_block'].x = settings.CENTER_X
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

    def _get_swimmer_animation_state(self):
        if not self.not_hit:  # Hit state
            if self.game_actors.push_powerup_active:
                return "swimmer_push_hit_states"
            return "swimmer_states_hit"

        # Normal state
        if self.game_actors.push_powerup_active:
            return "swimmer_push_states"

        # Handle inversion
        suffix = "_inv_states" if self.inversion_active else "_states"
        return f"swimmer{suffix}"

    def _animate_swimmer(self):
        state_key =self._get_swimmer_animation_state()
        swimmer_states = self.moving_actors_states['game_states'][state_key]
        self.animate_actor(self.game_actors.swimmer, swimmer_states, update_interval=10)

    def moving_update_animations(self):
        for coin in self.game_actors.collectibles['coins']:
            self.animate_actor(coin, self.moving_actors_states["obstacle_states"]["coin_states"], update_interval=10)

        for powerup in self.game_actors.powerups["powerups"]:
            if hasattr(powerup, 'image'):
                if "score" in powerup.image:
                    self.animate_actor(powerup, self.moving_actors_states["powerup_states"]["score_powerup_states"], update_interval=3, wait_time=10)
                if "speed" in powerup.image:
                    self.animate_actor(powerup, self.moving_actors_states["powerup_states"]["speed_powerup_states"], update_interval=10)
                if "push" in powerup.image:
                    self.animate_actor(powerup, self.moving_actors_states["powerup_states"]["push_powerup_states"], update_interval=30, wait_time=15)
                if "magnet" in powerup.image:
                    self.animate_actor(powerup, self.moving_actors_states["powerup_states"]["magnet_powerup_states"], update_interval=30, wait_time=15)

        self.animate_actor(self.game_actors.special["q_block"], self.moving_actors_states["game_states"]["q_block_states"], update_interval=15)
        self.animate_actor(self.game_actors.collectibles["glasses"], self.moving_actors_states["game_states"]["glasses_states"], update_interval=5, wait_time=30)
        self.animate_actor(self.game_actors.collectibles["swimmer_cap"], self.moving_actors_states["game_states"]["swimmer_cap_states"], update_interval=5, wait_time=30)
        self.game_actors.special['inversion_portal'].angle += 3

        suffix = "_inv_states" if  self.inversion_active else "_states"

        self._animate_swimmer()
        for bird in self.game_actors.bird_attack["birds"]:
            self.animate_actor(bird, self.moving_actors_states["game_states"]["bird_states"], update_interval=15)

        self.animate_actor(self.game_actors.obstacles['poop'], self.moving_actors_states["game_states"][f"poop{suffix}"], update_interval=20, wait_time=30)
        self.animate_actor(self.game_actors.obstacles["shark"], self.moving_actors_states["game_states"][f"shark{suffix}"], update_interval=5, wait_time=60)
        for log in self.game_actors.obstacles["logs"]:
            self.animate_actor(log, self.moving_actors_states["obstacle_states"][f"log{suffix}"], update_interval=10)
        if self.game_actors.obstacles["bear"].waiting_time > 0:
            pass
        else:
            self.animate_actor(self.game_actors.obstacles["bear"], self.moving_actors_states["game_states"][f"bear{suffix}"], update_interval=10)





    def stop_swimmer_hit_animation(self):
        self.not_hit = True

    def static_update_animations(self):
        for menu_item in self.game_actors.menu.values():
            if not menu_item.get("states"):
                continue
            try:
                self.animate_actor(menu_item["actor"], menu_item["states"], menu_item["update_interval"], menu_item["wait_time"])

            except Exception as e:
                print(f"Error animating menu item: {e}")
                continue