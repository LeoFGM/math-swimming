import random
import time
from random import randint
from pgzero import clock

from musicals import *


last_collision = 0

def speedrun_level_easy(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, sounds):
    global last_collision
    if game_clocks.action1 == 0:
        for i in range(0, 3): game_actors.new_log()
        for i in range(0, 1): game_actors.new_power_up()
    game_clocks.action1 = 1
    game_clocks.show_count = True
    ts = time.time()
    if game_clocks.show_count and game_clocks.action == 0:
        game_clocks.countup()
        game_clocks.action = 1
        enable_music_restore()
        for log in game_actors.logs: log.y = randint(-800, -300)
        game_actors.q_block.y = randint(-2000, -1600)
    if game_questions.answer == 'correct':
        game_clocks.count_max -= 5
        game_questions.answer = None
        game_questions.question_screen = None
    elif game_questions.answer == 'incorrect':
        game_clocks.count_max += 5
        game_questions.answer = None
        game_questions.question_screen = None
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
        if (game_actors.swimmer.colliderect(log)) and (ts - last_collision >= 3):
            game_clocks.count_max += 3
            last_collision = ts
            sounds.hit.play()
            actor_animation.not_hit = False
    for powerup in game_actors.powerups:
        actor_movement.actors_pos_x_fixated(powerup, 2, game_actors.powerup_collision, 3, first=-2000, last=-1600)
        for log in game_actors.logs:
            if powerup.colliderect(log): powerup.y += 75
            if game_actors.q_block.colliderect(log): log.y += 100
            if game_actors.q_block.colliderect(powerup): powerup.y += 75
        if game_actors.swimmer.colliderect(powerup):
            game_actors.powerup_collision = True
            game_clocks.count_max -= 5
            clock.schedule(game_actors.stop_powerup, 5)
            powerup.pos = random.choice([250, 400, 550]), randint(-2000, -1600)
            change_music_temporarily("stasis", 5, "strength")
    if game_actors.q_block.y < 600: game_actors.q_block.y += 2
    if game_actors.swimmer.colliderect(game_actors.q_block):
        game_actors.q_block.y = randint(-2000, -1600)
        current_screen = 'question_time'
        game_questions.question_screen = 'speed_easy'
    actor_animation.moving_update_animations()
    actor_movement.moving(game_actors.swimmer, game_actors.powerup_collision, quantity= 3, quantity2= 5)
    return current_screen

def points_level_easy(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, sounds):
    global last_collision
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
    if game_questions.answer == 'correct' and (game_clocks.count_down_max >= 5):
        game_clocks.score += 10
        game_questions.answer = None
        game_questions.question_screen = None
    elif game_questions.answer == 'incorrect':
        game_clocks.score -= 10
        game_questions.answer = None
        game_questions.question_screen = None
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
        if (game_actors.swimmer.colliderect(log)) and (ts - last_collision >= 3):
            game_clocks.score -= 3
            last_collision = ts
            sounds.hit.play()
            actor_animation.not_hit = False
    for coin in game_actors.coins:
        actor_movement.actors_random_pos(coin, 2, None, 3, first=-800, last=-100)
        for log in game_actors.logs:
            if coin.colliderect(log): coin.y += 30
            if game_actors.q_block.colliderect(log) and game_actors.q_block.y < 0: log.y += 100
            if game_actors.q_block.colliderect(coin) and game_actors.q_block.y < 0: coin.y += 75
        if game_actors.swimmer.colliderect(coin):
            game_clocks.score += 1
            sounds.coin.play()
            coin.pos = randint(175, 625), randint(-800, -200)
    actor_movement.actors_pos_x_fixated(game_actors.q_block, 2, None, 3, first= -2000, last= -1600)
    if game_actors.swimmer.colliderect(game_actors.q_block):
        game_actors.q_block.y = randint(-2000, -1600)
        current_screen = 'question_time'
        game_questions.question_screen = 'points_easy'
    actor_animation.moving_update_animations()
    actor_movement.moving(game_actors.swimmer, None, quantity= 3, quantity2=None)
    return current_screen

def speedrun_level_medium(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, sounds):
    global last_collision
    if game_clocks.action1 == 0:
        for i in range(0, 3): game_actors.new_log()
        for i in range(0, 1): game_actors.new_power_up()
    game_clocks.action1 = 1
    game_clocks.show_count = True
    ts = time.time()
    if game_clocks.show_count and game_clocks.action == 0:
        game_clocks.countup()
        game_clocks.action = 1
        enable_music_restore()
        for log in game_actors.logs: log.y = randint(-800, -300)
        game_actors.q_block.y = randint(-2000, -1600)
    if game_questions.answer == 'correct':
        game_clocks.count_max -= 5
        game_questions.answer = None
        game_questions.question_screen = None
    elif game_questions.answer == 'incorrect':
        game_clocks.count_max += 5
        game_questions.answer = None
        game_questions.question_screen = None
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
        if game_actors.shark.colliderect(log) or game_actors.shark.colliderect(game_actors.q_block):
            game_actors.shark.y += 75
            game_actors.shark.image = 'shark_14'
        if (game_actors.swimmer.colliderect(log)) and (ts - last_collision >= 3):
            game_clocks.count_max += 3
            last_collision = ts
            sounds.hit.play()
            actor_animation.not_hit = False
    for powerup in game_actors.powerups:
        actor_movement.actors_pos_x_fixated(powerup, 2.5, game_actors.powerup_collision, 3.5, first=-2400, last=-2000)
        for log in game_actors.logs:
            if powerup.colliderect(log): powerup.y += 75
            if game_actors.q_block.colliderect(log): log.y += 100
            if game_actors.q_block.colliderect(powerup): powerup.y += 75
        if game_actors.swimmer.colliderect(powerup):
            game_actors.powerup_collision = True
            powerup.pos = random.choice([250, 400, 550]), randint(-800, -500)
            game_clocks.count_max -= 5
            clock.schedule_unique(game_actors.stop_powerup, 5.0)
            change_music_temporarily("stasis", 5, "monster")
    actor_movement.actors_pos_x_fixated(game_actors.shark, 2.5, game_actors.powerup_collision, 3.5, first=-800, last=-600)
    if game_actors.shark.colliderect(game_actors.swimmer) and not game_actors.shark.image == "shark_14":
        game_clocks.count_max += 3
        sounds.sharkbite.set_volume(0.5)
        sounds.sharkbite.play()
        game_actors.shark.image = "shark_14"
        game_actors.shark.pos = random.choice([250, 400, 550]), randint(-800, -500)
    actor_movement.actors_pos_x_fixated(game_actors.q_block, 2.5, game_actors.powerup_collision, 3.5, first= -2000, last= -1600)
    if game_actors.swimmer.colliderect(game_actors.q_block):
        game_actors.q_block.y = randint(-2000, -1600)
        current_screen = 'question_time'
        game_questions.question_screen = 'speed_medium'
    actor_animation.moving_update_animations()
    actor_movement.moving(game_actors.swimmer, game_actors.powerup_collision, quantity=4, quantity2=6)
    return current_screen

def points_level_medium(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, sounds):
    global last_collision
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
    if game_questions.answer == 'correct' and (game_clocks.count_down_max >= 5):
        game_clocks.score += 10
        game_questions.answer = None
        game_questions.question_screen = None
    elif game_questions.answer == 'incorrect':
        game_clocks.score -= 10
        game_questions.answer = None
        game_questions.question_screen = None
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
        if (game_actors.swimmer.colliderect(log)) and (ts - last_collision >= 3):
            game_clocks.score -= 3
            last_collision = ts
            sounds.hit.play()
            actor_animation.not_hit = False
    for i, coin in enumerate(game_actors.coins):
        actor_movement.actors_random_pos(coin, 2.5, None, 3.5, first = -800, last = -100)
        for log in game_actors.logs:
            if coin.colliderect(log): coin.y += 30
            if game_actors.q_block.colliderect(log) and game_actors.q_block.y < 0: log.y += 100
            if game_actors.q_block.colliderect(coin) and game_actors.q_block.y < 0: coin.y += 75
        if game_actors.swimmer.colliderect(coin):
            game_clocks.score += 1
            sounds.coin.play()
            coin.pos = randint(175, 625), randint(-800, -200)
    actor_movement.actors_pos_x_fixated(game_actors.q_block, 2.5, None, 3.5, first= -2000, last= -1600)
    if game_actors.swimmer.colliderect(game_actors.q_block):
        game_actors.q_block.y = randint(-2000, -1600)
        current_screen = 'question_time'
        game_questions.question_screen = 'points_medium'
    actor_animation.moving_update_animations()
    actor_movement.moving(game_actors.swimmer, None, quantity= 4, quantity2=None)
    return current_screen