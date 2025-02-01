import random
import time
from random import randint
from pgzero import clock

from musicals import *
from utils import index_lists

last_collision = 0

def speedrun_level_easy(game_clocks, actors, game_questions, current_screen, sounds):
    global last_collision
    if game_clocks.action1 == 0:
        for i in range(0, 3):
            actors.new_log()
        for i in range(0, 1):
            actors.new_power_up()
    game_clocks.action1 = 1
    index_lists(actors.logs)
    game_clocks.show_count = True
    ts = time.time()
    if game_clocks.show_count and game_clocks.action == 0:
        game_clocks.countup()
        game_clocks.action = 1
        for log in actors.logs:
            log.y = randint(-800, -300)
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
    if actors.not_hit:
        if actors.number_of_updates_swimmer == 10:
            actors.actors_image_change(actors.swimmer, actors.swimmer_states)
            actors.number_of_updates_swimmer = 0
        else:
            actors.number_of_updates_swimmer += 1
    if not actors.not_hit:
        if actors.hit_updates == 6:
            actors.actors_image_change(actors.swimmer, actors.swimmer_states_hit)
            actors.hit_updates = 0
        else:
            actors.hit_updates += 1
            clock.schedule(actors.stop_swimmer_hit_animation, 3)
    for i, log in enumerate(actors.logs):
        if log.y < 600 and not actors.powerup_collision:
            log.y += 2
        elif log.y < 600 and actors.powerup_collision:
            log.y += 3
        else:
            max_attemps = 50
            attemps = 0
            while attemps < max_attemps:
                log.y = randint(-800, -500)
                if all(abs(log.y - other_log.y) > 200 for j, other_log in enumerate(actors.logs) if j != i):
                    break
                attemps += 1
            if attemps == max_attemps:
                log.y = -800
        if actors.number_of_updates_log == 10:
            actors.actors_image_change(log, actors.log_states)
            actors.number_of_updates_log = 0
        else:
            actors.number_of_updates_log += 1
        if (actors.swimmer.colliderect(log)) and (ts - last_collision >= 3):
            game_clocks.count_max += 3
            last_collision = ts
            sounds.hit.play()
            actors.not_hit = False
    for powerup in actors.powerups:
        if powerup.y < 600 and not actors.powerup_collision:
            powerup.y += 2
        elif powerup.y < 0 and actors.powerup_collision:
            powerup.pos = random.choice([250, 400, 550]), randint(-800, -500)
        else:
            powerup.pos = random.choice([250, 400, 550]), randint(-800, -500)
        if actors.number_of_updates_powerup == 10:
            actors.actors_image_change(powerup, actors.powerup_states)
            actors.number_of_updates_powerup = 0
        else:
            actors.number_of_updates_powerup += 1
        for log in actors.logs:
            if powerup.colliderect(log):
                powerup.y += 75
            if actors.q_block.colliderect(log):
                log.y += 100
            if actors.q_block.colliderect(powerup):
                powerup.y += 75
        if actors.swimmer.colliderect(powerup):
            actors.powerup_collision = True
            game_clocks.count_max -= 5
            clock.schedule(actors.stop_powerup, 5)
            change_music_temporarily("stasis", 5, "strength", game_clocks)
    if actors.q_block.y < 600:
        actors.q_block.y += 2
        if actors.number_of_updates_block == 15:
            actors.actors_image_change(actors.q_block, actors.q_block_states)
            actors.number_of_updates_block = 0
        else:
            actors.number_of_updates_block += 1
    else:
        actors.q_block.y = randint(-2000, -1600)
    if actors.swimmer.colliderect(actors.q_block):
        actors.q_block.y = randint(-2000, -1600)
        current_screen = 'question_time'
        game_questions.question_screen = 'speed_easy'
    actors.moving(actors.swimmer, actors.powerup_collision, quantity= 3, quantity2= 5)
    return current_screen

def points_level_easy(game_clocks, actors, game_questions, current_screen, sounds):
    global last_collision
    if game_clocks.action1 == 0:
        for i in range(0, 3):
            actors.new_log()
        for i in range(0, 20):
            actors.new_coin()
    game_clocks.action1 = 1
    index_lists(actors.logs)
    game_clocks.show_count = True
    ts = time.time()
    if game_clocks.show_count and game_clocks.action == 0:
        game_clocks.countdown()
        game_clocks.action = 1
        for log in actors.logs:
            log.y = randint(-800, -300)
    if game_questions.answer == 'correct' and (game_clocks.count_down_max >= 5):
        game_clocks.score += 10
        game_questions.answer = None
        game_questions.question_screen = None
    elif game_questions.answer == 'incorrect':
        game_clocks.score -= 10
        game_questions.answer = None
        game_questions.question_screen = None
    if game_clocks.count_down_max == 0:
        current_screen = 'gameover_points'
    if actors.not_hit:
        if actors.number_of_updates_swimmer == 10:
            actors.actors_image_change(actors.swimmer, actors.swimmer_states)
            actors.number_of_updates_swimmer = 0
        else:
            actors.number_of_updates_swimmer += 1
    if not actors.not_hit:
        if actors.hit_updates == 6:
            actors.actors_image_change(actors.swimmer, actors.swimmer_states_hit)
            actors.hit_updates = 0
        else:
            actors.hit_updates += 1
        clock.schedule(actors.stop_swimmer_hit_animation, 3)
    for i, log in enumerate(actors.logs):
        if log.y < 600:
            log.y += 2
        else:
            max_attemps = 50
            attemps = 0
            while attemps < max_attemps:
                log.y = randint(-800, -500)
                if all(abs(log.y - other_log.y) > 200 for j, other_log in enumerate(actors.logs) if j != i):
                    break
                attemps += 1
            if attemps == max_attemps:
                log.y = -800
        if actors.number_of_updates_log == 10:
            actors.actors_image_change(log, actors.log_states)
            actors.number_of_updates_log = 0
        else:
            actors.number_of_updates_log += 1
        if (actors.swimmer.colliderect(log)) and (ts - last_collision >= 3):
            game_clocks.score -= 3
            last_collision = ts
            sounds.hit.play()
            actors.not_hit = False
    for coin in actors.coins:
        if coin.y < 600:
            coin.y += 2
        else:
            coin.pos = randint(175, 625), randint(-800, -100)
        for log in actors.logs:
            if coin.colliderect(log):
                coin.y += 30
            if actors.q_block.colliderect(log) and actors.q_block.y < 0:
                log.y += 100
            if actors.q_block.colliderect(coin) and actors.q_block.y < 0:
                coin.y += 75
        if actors.number_of_updates_coin == 10:
            actors.actors_image_change(coin, actors.coin_states)
            actors.number_of_updates_coin = 0
        else:
            actors.number_of_updates_coin += 1
        if actors.swimmer.colliderect(coin):
            game_clocks.score += 1
            sounds.coin.play()
            coin.pos = randint(175, 625), randint(-800, -200)
    if actors.q_block.y < 600:
        actors.q_block.y += 2
        if actors.number_of_updates_block == 15:
            actors.actors_image_change(actors.q_block, actors.q_block_states)
            actors.number_of_updates_block = 0
        else:
            actors.number_of_updates_block += 1
    else:
        actors.q_block.y = randint(-2000, -1600)
    if actors.swimmer.colliderect(actors.q_block):
        actors.q_block.y = randint(-2000, -1600)
        current_screen = 'question_time'
        game_questions.question_screen = 'points_easy'
    actors.moving(actors.swimmer, None, quantity= 3, quantity2=None)
    return current_screen

def speedrun_level_medium(game_clocks, actors, game_questions, current_screen, sounds):
    global last_collision
    if game_clocks.action1 == 0:
        for i in range(0, 3):
            actors.new_log()
        for i in range(0, 1):
            actors.new_power_up()
    game_clocks.action1 = 1
    index_lists(actors.logs)
    game_clocks.show_count = True
    ts = time.time()
    if game_clocks.show_count and game_clocks.action == 0:
        game_clocks.countup()
        game_clocks.action = 1
        for log in actors.logs:
            log.y = randint(-800, -300)
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
    if actors.not_hit:
        if actors.number_of_updates_swimmer == 10:
            actors.actors_image_change(actors.swimmer, actors.swimmer_states)
            actors.number_of_updates_swimmer = 0
        else:
            actors.number_of_updates_swimmer += 1
    if not actors.not_hit:
        if actors.hit_updates == 6:
            actors.actors_image_change(actors.swimmer, actors.swimmer_states_hit)
            actors.hit_updates = 0
        else:
            actors.hit_updates += 1
            clock.schedule(actors.stop_swimmer_hit_animation, 3)
    for i, log in enumerate(actors.logs):
        if log.y < 600 and actors.powerup_collision:
            log.y += 3.5
        elif log.y < 600:
            log.y += 2.5
        else:
            max_attemps = 50
            attemps = 0
            while attemps < max_attemps:
                log.y = randint(-800, -500)
                if all(abs(log.y - other_log.y) > 200 for j, other_log in enumerate(actors.logs) if j != i):
                    break
                attemps += 1
            if attemps == max_attemps:
                log.y = -800
        if actors.number_of_updates_log == 10:
            actors.actors_image_change(log, actors.log_states)
            actors.number_of_updates_log = 0
        else:
            actors.number_of_updates_log += 1
        if actors.shark.colliderect(log) or actors.shark.colliderect(actors.q_block):
            actors.shark.y += 75
            actors.shark.image = 'shark_14'
        if (actors.swimmer.colliderect(log)) and (ts - last_collision >= 3):
            game_clocks.count_max += 3
            last_collision = ts
            sounds.hit.play()
            actors.not_hit = False
    for powerup in actors.powerups:
        if powerup.y < 600 and not actors.powerup_collision:
            powerup.y += 2.5
        else:
            powerup.pos = random.choice([250, 400, 550]), randint(-800, -500)
        if actors.number_of_updates_powerup == 10:
            actors.actors_image_change(powerup, actors.powerup_states)
            actors.number_of_updates_powerup = 0
        else:
            actors.number_of_updates_powerup += 1
        for log in actors.logs:
            if powerup.colliderect(log):
                powerup.y += 75
            if actors.q_block.colliderect(log):
                log.y += 100
            if actors.q_block.colliderect(powerup):
                powerup.y += 75
        if actors.swimmer.colliderect(powerup):
            actors.powerup_collision = True
            powerup.pos = random.choice([250, 400, 550]), randint(-800, -500)
            game_clocks.count_max -= 5
            clock.schedule_unique(actors.stop_powerup, 5.0)
            change_music_temporarily("stasis", 5, "monster", game_clocks)
    if actors.shark.y < 600:
        actors.shark.y += 3
        if actors.number_of_updates_shark == 5:
            actors.actors_image_change(actors.shark, actors.shark_states)
            actors.number_of_updates_shark = 0
            if actors.shark.image == "shark_14":
                actors.number_of_updates_shark = -60
        else:
            actors.number_of_updates_shark += 1
    else:
        actors.shark.pos = random.choice([250, 400, 550]), randint(-800, -500)
    if actors.shark.colliderect(actors.swimmer) and not actors.shark.image == "shark_14":
        game_clocks.count_max += 3
        sounds.sharkbite.set_volume(0.5)
        sounds.sharkbite.play()
        actors.shark.image = "shark_14"
        actors.shark.pos = random.choice([250, 400, 550]), randint(-800, -500)
    if actors.q_block.y < 600:
        actors.q_block.y += 2.5
        if actors.number_of_updates_block == 15:
            actors.actors_image_change(actors.q_block, actors.q_block_states)
            actors.number_of_updates_block = 0
        else:
            actors.number_of_updates_block += 1
    else:
        actors.q_block.y = randint(-2000, -1600)
    if actors.swimmer.colliderect(actors.q_block):
        actors.q_block.y = randint(-2000, -1600)
        current_screen = 'question_time'
        game_questions.question_screen = 'speed_medium'
    actors.moving(actors.swimmer, actors.powerup_collision, quantity=4, quantity2=6)
    return current_screen