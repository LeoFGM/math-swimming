from random import randint

class CompActors:
    def __init__(self, game_actors):
        self.bear = game_actors.bear
        self.bear_states = game_actors.get_moving_actors_states()["game_states"]["bear_states"]
        self.poop = game_actors.poop
        self.poop_states = game_actors.get_moving_actors_states()["game_states"]["poop_states"]
        self.pooping_pos = randint(200, 400)
        self.poop_pos = "not_pooping"

    def pooping(self, actor_animation):
        if self.bear.waiting_time > 0:
            self.bear.waiting_time -= 1
            return

        if self.bear.y == self.pooping_pos:
            self.bear.waiting_time = 30
            if self.bear.x == 110:
                self.bear.image = "bear_inv_poop_right" if actor_animation.inversion_active else "bear_poop_right"
                self.poop.pos = self.bear.x + 140, self.bear.y
            elif self.bear.x == 700:
                self.bear.image = "bear_inv_poop_left" if actor_animation.inversion_active else "bear_poop_left"
                self.poop.pos = self.bear.x - 150, self.bear.y
            self.poop_pos = "pooping_time"

    def bear_actions(self, actor_movement, comp_actors, game_actors, sounds, dt):
        if game_actors.bear.waiting_time > 0:
            if game_actors.bear.waiting_time == 30:
                sounds.fart.set_volume(0.4)
                sounds.fart.play()
            elif game_actors.bear.waiting_time == 10:
                sounds.water_splash.set_volume(0.2)
                sounds.water_splash.play()
        else:
            actor_movement.reposition_actors(game_actors, dt, comp_actors.bear, quantity=1)
        if 630 > game_actors.poop.y > 0:
            if "poop" in game_actors.bear.image:
                game_actors.poop.y += 0.5
            else:
                game_actors.poop.y += 2.5
        else:
            comp_actors.poop_pos = "not_pooping"
            game_actors.poop.y = -5000


