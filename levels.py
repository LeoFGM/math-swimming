import random
import time
from random import randint
from pgzero import clock

from musicals import *




def speedrun_level_easy(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, sounds):
    if game_clocks.action1 == 0:
        for i in range(0, 3): game_actors.new_log()
        for i in range(0, 1): game_actors.new_power_up(image='speed_powerup')
    game_clocks.action1 = 1
    game_clocks.show_count = True
    ts = time.time()
    if game_clocks.show_count and game_clocks.action == 0:
        game_clocks.countup()
        game_clocks.action = 1
        enable_music_restore()
        for log in game_actors.logs: log.y = randint(-800, -300)
        game_actors.q_block.y = randint(-2000, -1600)
    game_questions.analyze_answer_points(game_clocks)
    if game_clocks.count >= game_clocks.count_max:
        current_screen = 'gameover_speed'
        disable_music_restore()
    if not actor_animation.not_hit: clock.schedule(actor_animation.stop_swimmer_hit_animation, 3)
    for i, log in enumerate(game_actors.logs):
        if log.y < 600 and not game_actors.powerup_collision:
            log.y += 2
        elif log.y < 600 and game_actors.powerup_collision:
            log.y += 3
        else:
            max_attemps = 50
            attemps = 0
            while attemps < max_attemps:
                log.y = randint(-800, -500)
                if all(abs(log.y - other_log.y) > 200 for j, other_log in enumerate(game_actors.logs) if j != i):
                    break
                attemps += 1
            if attemps == max_attemps:
                log.y = -800
        actor_movement.log_collision(actor_animation, game_actors, game_clocks, log, sounds, ts)
    for powerup in game_actors.powerups:
        actor_movement.actors_pos_x_fixated(powerup, 2, game_actors.powerup_collision, 3, first=-2000, last=-1600)
        actor_movement.speed_powerup_collision(game_actors, game_clocks, powerup, "stasis", 5, "strength", clock)
    actor_movement.actors_pos_x_fixated(game_actors.q_block, 2, game_actors.powerup_collision, 3, first=-2000, last=-1600)
    current_screen = actor_movement.q_block_collision(current_screen, game_actors, game_questions, q_screen='speed_easy')
    actor_movement.handle_all_collisions(excluded_actor=game_actors.swimmer)
    actor_animation.moving_update_animations()
    actor_movement.moving(game_actors.swimmer, game_actors.powerup_collision, quantity= 3, quantity2= 5)
    return current_screen




def points_level_easy(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, sounds):
    if game_clocks.action1 == 0:
        for i in range(0, 3): game_actors.new_log()
        for i in range(0, 20): game_actors.new_coin()
    game_clocks.action1 = 1
    game_clocks.show_count = True
    ts = time.time()
    if game_clocks.show_count and game_clocks.action == 0:
        game_clocks.countdown()
        game_clocks.action = 1
        for log in game_actors.logs: log.y = randint(-800, -300)
        game_actors.q_block.y = randint(-2000, -1600)
    game_questions.analyze_answer_points(game_clocks)
    if game_clocks.count_down_max == 0: current_screen = 'gameover_points'
    if not actor_animation.not_hit: clock.schedule(actor_animation.stop_swimmer_hit_animation, 3)
    for i, log in enumerate(game_actors.logs):
        if log.y < 600:
            log.y += 2
        else:
            max_attemps = 50
            attemps = 0
            while attemps < max_attemps:
                log.y = randint(-800, -500)
                if all(abs(log.y - other_log.y) > 200 for j, other_log in enumerate(game_actors.logs) if j != i):
                    break
                attemps += 1
            if attemps == max_attemps:
                log.y = -800
        actor_movement.log_collision(actor_animation, game_actors, game_clocks, log, sounds, ts)
    for coin in game_actors.coins:
        actor_movement.actors_random_pos(coin, 2, None, 3, first=-800, last=-100)
        if game_actors.swimmer.colliderect(coin):
            game_clocks.score += 1
            sounds.coin.play()
            coin.pos = randint(175, 625), randint(-800, -200)
    actor_movement.actors_pos_x_fixated(game_actors.q_block, 2, None, 3, first= -2000, last= -1600)
    current_screen = actor_movement.q_block_collision(current_screen, game_actors, game_questions, q_screen='points_easy')
    actor_movement.handle_all_collisions(excluded_actor=game_actors.swimmer)
    actor_animation.moving_update_animations()
    actor_movement.moving(game_actors.swimmer, None, quantity= 3, quantity2=None)
    return current_screen

def speedrun_level_medium(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, sounds):
    if game_clocks.action1 == 0:
        for i in range(0, 3): game_actors.new_log()
        for i in range(0, 1): game_actors.new_power_up(image='speed_powerup')
    game_clocks.action1 = 1
    game_clocks.show_count = True
    ts = time.time()
    if game_clocks.show_count and game_clocks.action == 0:
        game_clocks.countup()
        game_clocks.action = 1
        enable_music_restore()
        for log in game_actors.logs: log.y = randint(-800, -300)
        game_actors.q_block.y = randint(-2000, -1600)
    game_questions.analyze_answer_points(game_clocks)
    if game_clocks.count >= game_clocks.count_max:
        current_screen = 'gameover_speed'
        disable_music_restore()
    if not actor_animation.not_hit: clock.schedule(actor_animation.stop_swimmer_hit_animation, 3)
    for i, log in enumerate(game_actors.logs):
        if log.y < 600 and game_actors.powerup_collision:
            log.y += 3.5
        elif log.y < 600:
            log.y += 2.5
        else:
            max_attemps = 50
            attemps = 0
            while attemps < max_attemps:
                log.y = randint(-800, -500)
                if all(abs(log.y - other_log.y) > 200 for j, other_log in enumerate(game_actors.logs) if j != i):
                    break
                attemps += 1
            if attemps == max_attemps:
                log.y = -800
        actor_movement.log_collision(actor_animation, game_actors, game_clocks, log, sounds, ts)
    for powerup in game_actors.powerups:
        actor_movement.actors_pos_x_fixated(powerup, 2.5, game_actors.powerup_collision, 3.5, first=-2400, last=-2000)
        actor_movement.speed_powerup_collision(game_actors, game_clocks, powerup, "stasis", 5, "monster", clock)
    actor_movement.actors_pos_x_fixated(game_actors.shark, 2.5, game_actors.powerup_collision, 3.5, first=-800, last=-600)
    actor_movement.shark_collision(game_actors, game_clocks, sounds)
    actor_movement.actors_pos_x_fixated(game_actors.q_block, 2.5, game_actors.powerup_collision, 3.5, first= -2000, last= -1600)
    current_screen = actor_movement.q_block_collision(current_screen, game_actors, game_questions, q_screen='speed_medium')
    actor_movement.handle_all_collisions(excluded_actor=game_actors.swimmer)
    actor_animation.moving_update_animations()
    actor_movement.moving(game_actors.swimmer, game_actors.powerup_collision, quantity=4, quantity2=6)
    return current_screen

def points_level_medium(game_clocks, game_actors, comp_actors, actor_movement, actor_animation, game_questions, current_screen, sounds):
    if game_clocks.action1 == 0:
        for i in range(0, 3): game_actors.new_log()
        for i in range(0, 20): game_actors.new_coin()
        for i in range(0, 1): game_actors.new_power_up(image='score_powerup')
    game_clocks.action1 = 1
    game_clocks.show_count = True
    ts = time.time()
    if game_clocks.show_count and game_clocks.action == 0:
        game_clocks.countdown()
        game_clocks.action = 1
        for log in game_actors.logs: log.y = randint(-800, -300)
        game_actors.q_block.y = randint(-2000, -1600)
    game_questions.analyze_answer_points(game_clocks)
    if game_clocks.count_down_max == 0: current_screen = 'gameover_points'
    if not actor_animation.not_hit: clock.schedule(actor_animation.stop_swimmer_hit_animation, 3)
    for i, log in enumerate(game_actors.logs):
        if log.y < 600:
            log.y += 2.5
        else:
            max_attemps = 50
            attemps = 0
            while attemps < max_attemps:
                log.y = randint(-800, -500)
                if all(abs(log.y - other_log.y) > 200 for j, other_log in enumerate(game_actors.logs) if j != i):
                    break
                attemps += 1
            if attemps == max_attemps:
                log.y = -800
        actor_movement.log_collision(actor_animation, game_actors, game_clocks, log, sounds, ts)
    for i, coin in enumerate(game_actors.coins):
        actor_movement.actors_random_pos(coin, 2.5, None, 3.5, first = -800, last = -100)
        if game_actors.swimmer.colliderect(coin):
            if game_actors.powerup_collision:
                game_clocks.score += 2
            else:
                game_clocks.score += 1
            sounds.coin.play()
            coin.pos = randint(175, 625), randint(-800, -200)
    actor_movement.actors_pos_x_fixated(game_actors.q_block, 2.5, None, 3.5, first= -2000, last= -1600)
    if game_actors.bear.waiting_time > 0:
        if game_actors.bear.waiting_time == 30:
            sounds.fart.set_volume(0.4)
            sounds.fart.play()
        elif game_actors.bear.waiting_time == 10:
            sounds.water_splash.set_volume(0.2)
            sounds.water_splash.play()
    else:
        actor_movement.actors_pos_x_fixated(game_actors.bear, 1, None, 3.5, first=-1000, last=-800, a=110, b=700, c=700)
    if 630 > game_actors.poop.y > 0:
        if "poop" in game_actors.bear.image:
            game_actors.poop.y += 0.5
        else:
            game_actors.poop.y += 2.5
    else:
        comp_actors.poop_pos = "not_pooping"
        game_actors.poop.y = -5000
    actor_movement.poop_collision(game_actors, game_clocks, sounds)
    for powerup in game_actors.powerups:
        actor_movement.actors_pos_x_fixated(powerup, 2.5, None, 3.5, first=-2400, last=-2000)
        actor_movement.score_powerup_collision(game_actors, game_clocks, powerup, sounds, clock)
    current_screen = actor_movement.q_block_collision(current_screen, game_actors, game_questions, q_screen='points_medium')
    actor_movement.handle_all_collisions(excluded_actor=game_actors.swimmer)
    actor_animation.moving_update_animations()
    actor_movement.moving(game_actors.swimmer, None, quantity= 4, quantity2=None)
    return current_screen


