import random
import time
from random import randint
from pgzero import clock
from constants import QuestionStates, GameState


def speedrun_level_easy(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, game_screens, music_actions, sounds):
    if game_clocks.action == 0:
        for x in (250 + i * 150 for i in range(0, 3)):
            game_actors.actor_storage.new_actor(image_name="log", position=(x, randint(-800, -300)), actor_list=game_actors.logs, special_x=x, first=-800, last=-300)
        for i in range(0, 1):
            game_actors.actor_storage.new_actor(image_name='speed_powerup', position=(random.choice(actor_movement.DEFAULT_POSITIONS), randint(-1600, -800)), actor_list=game_actors.powerups, first=-1600, last=-800)
        game_clocks.countup()
        music_actions.enable_music_restore()
        actor_movement.reset_actors_position(actor_animation, game_actors.q_block, game_actors.logs, game_actors.powerups, game_actors.inversion_portal)

    game_clocks.action = 1
    game_clocks.show_count = True
    ts = time.time()

    if game_clocks.count >= game_clocks.count_max:
        current_screen = GameState.GAMEOVER_SPEED
        music_actions.disable_music_restore()
        game_clocks.level_elapsed_time = game_clocks.get_elapsed_time()
    if not actor_animation.not_hit: clock.schedule(actor_animation.stop_swimmer_hit_animation, 3)

    #Collisions with swimmer
    actor_movement.log_collision(game_actors, game_clocks, sounds, ts)
    actor_movement.speed_powerup_collision(game_actors, game_clocks, "stasis", 5, "strength", music_actions, clock)
    actor_movement.glasses_collision(game_actors, game_clocks, current_screen, sounds)
    actor_movement.inversion_portal_collision(game_actors, game_clocks, actor_animation, game_screens.transition_manager, sounds, game_actors.q_block, game_actors.logs, game_actors.powerups)
    actor_movement.handle_all_collisions(excluded_actor=game_actors.swimmer)
    current_screen = actor_movement.q_block_collision(current_screen, game_actors, game_questions, q_screen=QuestionStates.SPEED_EASY)

    #Actors movement
    actor_movement.reposition_actors(game_actors, actor_animation,
        game_actors.q_block, game_actors.powerups, game_actors.logs, game_actors.glasses, game_actors.inversion_portal,
        quantity=2, special_effect=game_actors.powerup_collision, alt_quantity=3)
    actor_movement.move_swimmer(actor_animation, game_actors.swimmer, game_actors.powerup_collision, normal_speed= 3, fast_speed= 5)

    #Actors animation
    actor_animation.moving_update_animations()
    return current_screen

def points_level_easy(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, game_screens, sounds):
    if game_clocks.action == 0:
        for x in (250 + i * 150 for i in range(0, 3)):
            game_actors.actor_storage.new_actor(image_name="log", position=(x, randint(-800, -300)), actor_list=game_actors.logs, special_x=x, first=-800, last=-300)
        for i in range(0, 20): game_actors.actor_storage.new_actor(image_name="coin", position=(randint(175, 625), randint(-800, -100)), actor_list=game_actors.coins, first=-800, last=-100)

        game_clocks.countdown()
        actor_movement.reset_actors_position(actor_animation, game_actors.q_block, game_actors.logs, game_actors.coins, game_actors.glasses, game_actors.inversion_portal)

    game_clocks.action = 1
    game_clocks.show_count = True
    ts = time.time()

    if game_clocks.count_down_max == 0: current_screen = GameState.GAMEOVER_POINTS
    if not actor_animation.not_hit: clock.schedule(actor_animation.stop_swimmer_hit_animation, 3)

    #Collisions with swimmer
    actor_movement.log_collision(game_actors, game_clocks, sounds, ts)
    actor_movement.coin_collision(game_actors, game_clocks, sounds)
    actor_movement.glasses_collision(game_actors, game_clocks, current_screen, sounds)
    actor_movement.inversion_portal_collision(game_actors, game_clocks, actor_animation, game_screens.transition_manager, sounds, game_actors.q_block, game_actors.logs, game_actors.powerups)
    actor_movement.handle_all_collisions(excluded_actor=game_actors.swimmer)
    current_screen = actor_movement.q_block_collision(current_screen, game_actors, game_questions, q_screen=QuestionStates.POINTS_EASY)

    # Actors movement
    actor_movement.move_swimmer(actor_animation, game_actors.swimmer, None, normal_speed= 3, fast_speed=None)
    actor_movement.reposition_actors(game_actors, actor_animation, game_actors.q_block, game_actors.coins, game_actors.logs, game_actors.glasses, game_actors.inversion_portal, quantity=2)

    #Actors animation
    actor_animation.moving_update_animations()
    return current_screen

def speedrun_level_medium(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, game_screens, music_actions, sounds, dt):
    if game_clocks.action == 0:
        for x in (250 + i * 150 for i in range(0, 3)):
            game_actors.actor_storage.new_actor(image_name="log", position=(x, randint(-800, -500)), actor_list=game_actors.logs, special_x=x, first=-800, last=-500)
        for i in range(0, 1):
            game_actors.actor_storage.new_actor(image_name='speed_powerup', position=(random.choice(actor_movement.DEFAULT_POSITIONS), randint(-3000, -1500)), actor_list=game_actors.powerups, first=-3000, last=-1500)
            game_actors.actor_storage.new_actor(image_name='push_powerup', position=(random.choice(actor_movement.DEFAULT_POSITIONS), randint(-3200, -1800)), actor_list=game_actors.powerups, first=-3200, last=-1800)
        game_clocks.countup()
        music_actions.enable_music_restore()
        actor_movement.reset_actors_position(actor_animation, game_actors.q_block, game_actors.logs, game_actors.powerups, game_actors.shark, game_actors.glasses, game_actors.inversion_portal)

    game_clocks.action = 1
    game_clocks.show_count = True
    ts = time.time()

    if game_clocks.count >= game_clocks.count_max:
        current_screen = GameState.GAMEOVER_SPEED
        music_actions.disable_music_restore()
        game_clocks.level_elapsed_time = game_clocks.get_elapsed_time()
    if not actor_animation.not_hit: clock.schedule(actor_animation.stop_swimmer_hit_animation, 3)

    #Collisions with swimmer
    actor_movement.log_collision(game_actors, game_clocks, sounds, ts)
    actor_movement.speed_powerup_collision(game_actors, game_clocks, "stasis", 5, "monster", music_actions, clock)
    actor_movement.shark_collision(game_actors, game_clocks, sounds)
    actor_movement.glasses_collision(game_actors, game_clocks, current_screen, sounds)
    actor_movement.inversion_portal_collision(game_actors, game_clocks, actor_animation, game_screens.transition_manager, sounds, game_actors.q_block, game_actors.logs, game_actors.powerups)
    actor_movement.push_powerup_collision(game_actors, game_clocks, sounds)
    current_screen = actor_movement.q_block_collision(current_screen, game_actors, game_questions, q_screen=QuestionStates.SPEED_MEDIUM)
    actor_movement.handle_all_collisions(excluded_actor=game_actors.swimmer)

    # Actors movement
    actor_movement.reposition_actors(game_actors, actor_animation, dt, game_actors.logs, game_actors.q_block, game_actors.shark, game_actors.powerups, game_actors.glasses, game_actors.inversion_portal, quantity=2.5, special_effect=game_actors.powerup_collision, alt_quantity=3.5)

    actor_movement.move_swimmer(actor_animation, game_actors.swimmer, objects=game_actors.powerup_collision, normal_speed=4, fast_speed=6)


    # Actors animation
    actor_animation.moving_update_animations()
    return current_screen

def points_level_medium(game_clocks, game_actors, comp_actors, actor_movement, actor_animation, game_questions, current_screen, game_screens, sounds, dt):
    if game_clocks.action == 0:
        for x in (250 + i * 150 for i  in range(0, 3)):
            game_actors.actor_storage.new_actor(image_name="log", position=(x, randint(-800, -500)), actor_list=game_actors.logs, special_x=x, first=-800, last=-500)
        for i in range(0, 20): game_actors.actor_storage.new_actor(image_name="coin", position=(randint(175, 625), randint(-800, -300)), actor_list=game_actors.coins, first=-800, last=-300)
        for i in range(0, 1):
            game_actors.actor_storage.new_actor(image_name='score_powerup', position=(random.choice(actor_movement.DEFAULT_POSITIONS), randint(-2000, -1000)), actor_list=game_actors.powerups, x_locked=True, first=-2000, last=-1000)
            game_actors.actor_storage.new_actor(image_name='push_powerup', position=(random.choice(actor_movement.DEFAULT_POSITIONS), randint(-3200, -1800)), actor_list=game_actors.powerups, first=-3200, last=-1800)

        game_clocks.countdown()
        actor_movement.reset_actors_position(actor_animation, game_actors.q_block, game_actors.powerups, game_actors.logs, game_actors.glasses, game_actors.inversion_portal)

    game_clocks.action = 1
    game_clocks.show_count = True
    ts = time.time()

    if game_clocks.count_down_max == 0: current_screen = GameState.GAMEOVER_POINTS
    if not actor_animation.not_hit: clock.schedule(actor_animation.stop_swimmer_hit_animation, 3)

    #Comp actor's actions
    comp_actors.bear_actions(actor_movement, comp_actors, game_actors, sounds, dt)

    #Collisions with swimmer
    actor_movement.poop_collision(game_actors, game_clocks, sounds)
    actor_movement.score_powerup_collision(game_actors, game_clocks, sounds, clock)
    actor_movement.coin_collision(game_actors, game_clocks, sounds)
    actor_movement.log_collision(game_actors, game_clocks, sounds, ts)
    actor_movement.glasses_collision(game_actors, game_clocks, current_screen, sounds)
    actor_movement.inversion_portal_collision(game_actors, game_clocks, actor_animation, game_screens.transition_manager, sounds, game_actors.q_block, game_actors.logs, game_actors.powerups, game_actors.coins)
    actor_movement.push_powerup_collision(game_actors, game_clocks, sounds)
    current_screen = actor_movement.q_block_collision(current_screen, game_actors, game_questions, q_screen=QuestionStates.POINTS_MEDIUM)
    actor_movement.handle_all_collisions(excluded_actor=game_actors.swimmer)

    # Actors movement
    actor_movement.move_swimmer(actor_animation, game_actors.swimmer, None, normal_speed= 4, fast_speed=None)
    actor_movement.reposition_actors(game_actors, actor_animation, dt, game_actors.q_block, game_actors.powerups, game_actors.coins, game_actors.logs, game_actors.glasses, game_actors.inversion_portal, quantity=2.5)

    # Actors animation
    actor_animation.moving_update_animations()
    return current_screen








