from .background_manager import BackgroundManager
from .actor_movement import ActorMovementManager
from game.actors.systems.collision import CollisionManager


class ActorMovementInteractions:
    def __init__(self, actor_animation, transition_manager=None, config=None):
        self.background_manager = BackgroundManager()
        self.actor_movement_manager = ActorMovementManager()
        self.collision_manager = CollisionManager(
            actor_animation,
            self.background_manager,
            config=config,
            transition_manager=transition_manager,
            actor_movement_manager=self.actor_movement_manager
        )
        self.transition_manager = transition_manager
        self.config = config or {
            "default_positions": [250, 400, 550],
            "collision_cooldown": 3,
            "powerup_duration": 5}

    def set_background(self, screen):
        self.background_manager.set_background(screen)

    def moving_bg(self):
        self.background_manager.moving_bg()

    def move_swimmer(self, context, objects, normal_speed, fast_speed):
        self.actor_movement_manager.move_swimmer(context, objects, normal_speed, fast_speed)

    def reposition_actors(self, context, dt, *actors, quantity, special_effect=None, alt_quantity=None):
        self.actor_movement_manager.reposition_actors(context, dt, *actors, quantity=quantity, special_effect=special_effect, alt_quantity=alt_quantity)

    def update_push_animation(self, log, context, dt):
        self.actor_movement_manager.update_push_animation(log, context, dt)

    def reset_actors_position(self, context, *actors):
        self.actor_movement_manager.reset_actors_position(context, *actors)

    def handle_between_collisions(self, excluded_actor):
        self.collision_manager.handle_between_collisions(excluded_actor)

    def q_block_collision(self, context, q_screen):
        return self.collision_manager.q_block_collision(context, q_screen)

    def log_collision(self, context, ts):
        self.collision_manager.log_collision(context, ts)

    def speed_powerup_collision(self, context, new_music, duration, initial_music):
        self.collision_manager.speed_powerup_collision(context, new_music, duration, initial_music)

    def score_powerup_collision(self, context):
        self.collision_manager.score_powerup_collision(context)

    def coin_collision(self, context):
        self.collision_manager.coin_collision(context)

    def shark_collision(self, context):
        self.collision_manager.shark_collision(context)

    def poop_collision(self, context):
        self.collision_manager.poop_collision(context)

    def glasses_collision(self, context):
        self.collision_manager.glasses_collision(context)

    def inversion_portal_collision(self, context, *actors):
        self.collision_manager.inversion_portal_collision(context, *actors)

    def push_powerup_collision(self, context):
        self.collision_manager.push_powerup_collision(context)

    def swimmer_cap_collision(self, context):
        self.collision_manager.swimmer_cap_collision(context)

    def magnet_collision(self, context):
        self.collision_manager.magnet_collision(context)

    def update_magnet_effect(self, context, dt):
        self.actor_movement_manager.update_magnet_effect(context, dt)

    def handle_bird_attack_collisions(self, context):
        self.collision_manager.handle_bird_attack_collisions(context)
