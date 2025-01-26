import random
import threading
import pygame
import pgzrun
from random import randint, shuffle, choice, choices

from pygame.time import delay

from actors import GameActors
from settings import settings

from changevar import *
from utils import *
from questions import *

import time
import math

pygame.init()




#Music

music.set_volume(0.25)
music.play("loadscreen")

current_music = None
current_position = 0

MUSIC_FOLDER = "music"
MUSIC_EXTENSION = ".ogg"

def change_music_temporarily(new_music, duration, initial_music):
    global current_music, current_position
    print("function activated")
    if pygame.mixer.music.get_busy():
        current_music = initial_music
        current_position = pygame.mixer.music.get_pos()
        pygame.mixer.music.pause()

    #Pause current music
    pygame.mixer.music.pause()

    #Play new music
    print(f"Playing temporary music: {new_music}")
    pygame.mixer.music.load(f"{MUSIC_FOLDER}/{new_music}{MUSIC_EXTENSION}")
    pygame.mixer.music.play()
    pygame.mixer.music.fadeout(duration * 1000)

    #Unpause initial music
    def restore_music():
        global  current_music, current_position
        print(f"Restoring {initial_music}")
        pygame.mixer.music.stop()
        if current_music:
            pygame.mixer.music.load(f"{MUSIC_FOLDER}/{current_music}{MUSIC_EXTENSION}")
            pygame.mixer.music.play(start=current_position / 1000)

    def delayed_restore():
        time.sleep(duration)
        restore_music()

    threading.Thread(target=delayed_restore).start()


#Mouse interactions




#levels






game_clocks = GameClocks()

def speedrun_level_easy():
    global last_collision, current_screen
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
        game_clocks.count_max -= 10
        game_questions.answer = None
    elif game_questions.answer == 'incorrect':
        game_clocks.count_max += 10
        game_questions.answer = None
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
            change_music_temporarily("stasis", 5, "strength")
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
        game_questions.question_screen = 'speed'
    actors.moving(actors.swimmer, actors.powerup_collision, quantity= 3, quantity2= 5)

def points_level_easy():
    global current_screen, last_collision
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
    elif game_questions.answer == 'incorrect':
        game_clocks.score -= 10
        game_questions.answer = None
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
        game_questions.question_screen = 'points'
    actors.moving(actors.swimmer, None, quantity= 3, quantity2=None)

def speedrun_level_medium():
    global last_collision, current_screen
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
        game_clocks.count_max -= 10
        game_questions.answer = None
    elif game_questions.answer == 'incorrect':
        game_clocks.count_max += 10
        game_questions.answer = None
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
        if actors.shark.colliderect(log):
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
            change_music_temporarily("stasis", 5, "monster")
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
    actors.moving(actors.swimmer, actors.powerup_collision, quantity=4, quantity2=6)

#Drawing

actors = GameActors()
game_questions = GameQuestions()
current_screen = 'start'

#Game state variables

def draw():
    screen.clear()
    screen.blit("river", (0, 0))
    if current_screen == 'start':
        actors.draw_start_screen()
    elif current_screen == 'gamemode':
        actors.draw_gamemode_screen()
    elif current_screen == 'difficulty_speed' or current_screen == 'difficulty_points':
        actors.draw_difficulty_screen()
    elif current_screen == 'speedrun_easy':
        actors.set_background(screen)
        actors.swimmer.draw()
        actors.q_block.draw()
        screen.draw.text("Time: " + str(game_clocks.count), color="orange red", topleft=(20,20), fontsize=40)
        actors.create_actors(actors.logs)
        actors.create_actors(actors.powerups)
    elif current_screen == 'points_easy':
        actors.set_background(screen)
        actors.swimmer.draw()
        actors.q_block.draw()
        screen.draw.text("Time: " + str(game_clocks.count_down_max), color="orange red", topleft=(20,20), fontsize=40)
        screen.draw.text("Score: " + str(game_clocks.score), color="orange red", topleft=(670,20), fontsize=40)
        actors.create_actors(actors.logs)
        actors.create_actors(actors.coins)
    elif current_screen == 'speedrun_medium':
        actors.set_background(screen)
        actors.swimmer.draw()
        actors.shark.draw()
        actors.create_actors(actors.logs)
        actors.create_actors(actors.powerups)
        screen.draw.text("Time: " + str(game_clocks.count), color="orange red", topleft=(20,20), fontsize=40)
    elif current_screen == 'points_medium':
        actors.set_background(screen)
        actors.swimmer.draw()
        screen.draw.text("Time: " + str(game_clocks.count_down_max), color="orange red", topleft=(20,20), fontsize=40)
        screen.draw.text("Score: " + str(game_clocks.score), color="orange red", topleft=(670,20), fontsize=40)
    #Game over screens:
    elif current_screen == 'gameover_speed':
        actors.set_background(screen)
        screen.draw.text("You completed the level in: " + str(game_clocks.count) + " seconds!", color="black", center=settings.CENTER, fontsize=60)
        actors.goback.draw()
    elif current_screen == 'gameover_points':
        actors.set_background(screen)
        screen.draw.text("You ended with: " + str(game_clocks.score) + " points!", color="black", center=settings.CENTER, fontsize=60)
        actors.goback.draw()
    #Question screen
    elif current_screen == 'question_time':
        print(f"Question: {game_questions.questions_e[0]}")
        print(f"Type of question: {type(game_questions.questions_e[0])}")
        actors.set_background(screen)
        screen.draw.filled_rect(game_questions.main_box, "sky blue")
        screen.draw.filled_rect(game_questions.timer_box, "sky blue")
        for box in game_questions.answer_boxes:
            screen.draw.filled_rect(box, "medium slate blue")
        screen.draw.textbox(str(game_questions.time_left_e), game_questions.timer_box, color="black")
        screen.draw.textbox(game_questions.question_e[0], game_questions.main_box, color="black")
        for index, box in enumerate(game_questions.answer_boxes, start=1):
            screen.draw.textbox(game_questions.question_e[index], box, color="black")



def on_mouse_down(pos):
    global current_screen
    clicked_actor = actors.handle_mouse_down(pos)
    if clicked_actor == 'start' and current_screen == "start":
        sounds.select.play()
        current_screen = 'gamemode'
    elif clicked_actor == 'speedrun' and current_screen == "gamemode":
        sounds.select.play()
        current_screen = 'difficulty_speed'
    elif clicked_actor == 'pointsmania' and current_screen == "gamemode":
        sounds.select.play()
        current_screen = 'difficulty_points'
    elif clicked_actor == 'goback':
        sounds.goback.play()
        if current_screen == 'gameover_speed' or current_screen == 'gameover_points':
            music.play("loadscreen")
        game_clocks.reset_variables()
        game_questions.questions_e = game_questions.questions_e
        actors.x = 250
        actors.logs.clear()
        actors.coins.clear()
        actors.powerups.clear()
        current_screen = 'start'
    elif clicked_actor == 'easy' and (current_screen == 'difficulty_speed' or current_screen == 'difficulty_points'):
        shuffle(game_questions.questions_e)
        if current_screen == 'difficulty_speed':
            sounds.select.play()
            music.play("strength")
            current_screen = 'speedrun_easy'
        elif current_screen == 'difficulty_points':
            sounds.select.play()
            music.play("behemoth")
            current_screen = 'points_easy'
    elif clicked_actor == 'medium' and (current_screen == 'difficulty_speed' or current_screen == 'difficulty_points'):
        if current_screen == 'difficulty_speed':
            sounds.select.play()
            music.play("monster")
            current_screen = 'speedrun_medium'
        elif current_screen == 'difficulty_points':
            sounds.select.play()
            music.play("hero")
            current_screen = 'points_medium'
    elif current_screen == "question_time":
        for index, box in enumerate(game_questions.answer_boxes, start=1):
            print(f"Checking box {index} at position {pos}")
            if box.collidepoint(pos) and game_questions.question_screen == 'points':
                current_screen, game_questions.answer = game_questions.update_game_state_points(index, sounds)
                game_questions.question_e = game_questions.questions_e.pop(0)
                game_questions.questions_e.append(game_questions.question_e)
            elif box.collidepoint(pos) and game_questions.question_screen == 'speed':
                print(f"Box {index} clicked, updating game state")
                current_screen, game_questions.answer = game_questions.update_game_state_speed(index, sounds)
                game_questions.question_e = game_questions.questions_e.pop(0)
                game_questions.questions_e.append(game_questions.question_e)




def update():
    if current_screen == 'start':
        if actors.number_of_updates == 15:
            actors.actors_image_change(actors.gamename, actors.game_name_states)
            actors.number_of_updates = 0
        else:
            actors.number_of_updates += 1
    elif current_screen == 'gamemode':
        if actors.number_of_updates == 15:
            actors.actors_image_change(actors.gamemode, actors.gamemode_states)
            actors.number_of_updates = 0
        else:
            actors.number_of_updates += 1
    elif (current_screen == 'difficulty_speed') or (current_screen == 'difficulty_points'):
        if actors.number_of_updates1 == 3:
            actors.actors_image_change(actors.difficulty, actors.title_states_diff)
            actors.actors_image_change(actors.easy, actors.title_states_easy)
            actors.actors_image_change(actors.medium, actors.title_states_medium)
            actors.actors_image_change(actors.hard, actors.title_states_hard)
            actors.actors_image_change(actors.extreme, actors.title_states_extreme)
            if actors.easy.image == 'easy':
                actors.number_of_updates1 = -60
            else:
                actors.number_of_updates1 = 0
        else:
            actors.number_of_updates1 += 1
    elif current_screen == 'speedrun_easy':
        speedrun_level_easy()
        actors.moving_bg()
    elif current_screen == 'points_easy':
        points_level_easy()
        actors.moving_bg()
    elif current_screen == 'speedrun_medium':
        actors.moving_bg()
        speedrun_level_medium()
    elif current_screen == 'points_medium':
        actors.moving_bg()
    #Question interactions








pgzrun.go()
