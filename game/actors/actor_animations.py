

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
            self.animate_actor(coin, self.moving_actors_states["obstacle_states"]["coin_states"], update_interval=10)

        for log in self.moving_actors["logs"]:
            self.animate_actor(log, self.moving_actors_states["obstacle_states"]["log_states"], update_interval=10)

        for powerup in self.moving_actors["powerups"]:
            if "score" in powerup.image:
                self.animate_actor(powerup, self.moving_actors_states["powerup_states"]["score_powerup_states"], update_interval=3, wait_time=10)
            elif "speed" in powerup.image:
                self.animate_actor(powerup, self.moving_actors_states["powerup_states"]["speed_powerup_states"], update_interval=10)

        self.animate_actor(self.moving_actors["q_block"], self.moving_actors_states["game_states"]["q_block_states"], update_interval=15)
        self.animate_actor(self.moving_actors["shark"], self.moving_actors_states["game_states"]["shark_states"], update_interval=5, wait_time=60)

        if self.moving_actors["bear"].waiting_time > 0:
            pass
        else:
            self.animate_actor(self.moving_actors["bear"], self.moving_actors_states["game_states"]["bear_states"], update_interval=10)

        self.animate_actor(self.moving_actors["poop"], self.moving_actors_states["game_states"]["poop_states"], update_interval=20, wait_time=30)
        self.animate_actor(self.moving_actors["glasses"], self.moving_actors_states["game_states"]["glasses_states"], update_interval=5, wait_time=15)

        if not self.not_hit:
            self.animate_actor(self.moving_actors["swimmer"], self.moving_actors_states["game_states"]["swimmer_states_hit"], update_interval=10)
        else:
            self.animate_actor(self.moving_actors["swimmer"], self.moving_actors_states["game_states"]["swimmer_states"], update_interval=10)

    def stop_swimmer_hit_animation(self):
        self.not_hit = True

    def static_update_animations(self):
        static_actors = self.game_actors.get_static_actors()
        for actor, states, update_interval, wait_time in static_actors:
            self.animate_actor(actor, states, update_interval, wait_time)
