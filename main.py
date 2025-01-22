import pgzrun
from random import randint, shuffle
from actors import GameActors
from settings import settings

from changevar import *
from utils import *
from questions import *

import time
import math

#Clocks



#Variables reset



#Music

def change_music():
    music.play("strength")

musics = ["voltaic-gale", "stasis"]
music.set_volume(0.25)
music.play("loadscreen")

#Mouse interactions




#levels

def stop_powerup():
    global powerup_collision
    powerup_collision = False

def stop_swimmer_hit_animation():
    global hit_animation, not_hit
    not_hit = True

action_1 = 0
action_2 = 0

game_clocks = GameClocks()

def speedrun_level_easy():
    global action_2, show_count, action1,last_collision, not_hit, hit_animation, powerup
    global powerup_collision, logs_already_created, powerups_already_created, question_screen
    if action_2 == 0:
        if not logs_already_created:
            for i in range(0, 3):
                actors.new_log()
                logs_already_created = True
        if not powerups_already_created:
            for i in range(0, 1):
                actors.new_power_up()
            powerups_already_created = True
    action_2 = 1
    index_lists(actors.logs)
    game_clocks.show_count = True
    ts = time.time()
    if game_clocks.show_count and game_clocks.action1 == 0:
        game_clocks.countup()
        game_clocks.action1 = 1
        for log in actors.logs:
            log.y = randint(-800, -300)
    if game_questions.answer == 'correct' and ((game_clocks.count_max - game_clocks.count) >= 15):
        game_clocks.count_max -= 10
        game_questions.answer = None
    elif game_questions.answer == 'incorrect':
        game_clocks.count_max += 10
        game_questions.answer = None
    if game_clocks.count == game_clocks.count_max:
        actors.current_screen = 'gameover_speed'
    if not_hit:
        if actors.number_of_updates_swimmer == 10:
            actors.actors_image_change(actors.swimmer, actors.swimmer_states)
            actors.number_of_updates_swimmer = 0
        else:
            actors.number_of_updates_swimmer += 1
    if not not_hit:
        if actors.hit_updates == 6:
            actors.actors_image_change(actors.swimmer, actors.swimmer_states_hit)
            actors.hit_updates = 0
        else:
            actors.hit_updates += 1
            clock.schedule(stop_swimmer_hit_animation, 3)
    for log in actors.logs:
        if log.y < 600 and not powerup_collision:
            log.y += 2
        elif log.y < 600 and powerup_collision:
            log.y += 3
        else:
            log.y = randint(-800, -500)
        if actors.number_of_updates_log == 10:
            actors.actors_image_change(log, actors.log_states)
            actors.number_of_updates_log = 0
        else:
            actors.number_of_updates_log += 1
        if (actors.swimmer.colliderect(log)) and (ts - last_collision >= 3):
            game_clocks.count_max += 3
            last_collision = ts
            sounds.hit.play()
            not_hit = False
    for powerup in actors.powerups:
        if powerup.y < 600 and not powerup_collision:
            powerup.y += 2
        elif powerup.y < 0 and powerup_collision:
            powerup.y = randint(-800, -500)
        else:
            powerup.y = randint(-800, -500)
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
            powerup_collision = True
            game_clocks.count_max -= 5
            music.stop()
            music.play("stasis")
            music.fadeout(5)
            clock.schedule(stop_powerup, 5)
            clock.schedule(change_music, 5)
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
        actors.current_screen = 'question_time'
        game_questions.question_screen = 'speed'
    actors.moving(actors.swimmer, powerup_collision)

def points_level_easy():
    global action, action_1, show_count, score, number_of_updates_log, last_collision, hit_animation, hit_updates, number_of_updates_coin
    global points_easy_screen, not_hit, number_of_updates_swimmer, logs_already_created, coins_already_created, question_time, point_question_e
    if action_1 == 0:
        if not logs_already_created:
            for i in range(0, 3):
                actors.new_log()
            logs_already_created = True
        if not coins_already_created:
            for i in range(0, 20):
                actors.new_coin()
            coins_already_created = True
    action_1 = 1
    index_lists(actors.logs)
    show_count = True
    ts = time.time()
    if show_count and game_clocks.action == 0:
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
        actors.current_screen = 'gameover_points'
    if not_hit:
        if actors.number_of_updates_swimmer == 10:
            actors.actors_image_change(actors.swimmer, actors.swimmer_states)
            actors.number_of_updates_swimmer = 0
        else:
            actors.number_of_updates_swimmer += 1
    if not not_hit:
        if actors.hit_updates == 6:
            actors.actors_image_change(actors.swimmer, actors.swimmer_states_hit)
            actors.hit_updates = 0
        else:
            actors.hit_updates += 1
        clock.schedule(stop_swimmer_hit_animation, 3)
    for log in actors.logs:
        if log.y < 600:
            log.y += 2
        else:
            log.y = randint(-800, -500)
        if actors.number_of_updates_log == 10:
            actors.actors_image_change(log, actors.log_states)
            actors.number_of_updates_log = 0
        else:
            actors.number_of_updates_log += 1
        if (actors.swimmer.colliderect(log)) and (ts - last_collision >= 3):
            game_clocks.score -= 3
            last_collision = ts
            sounds.hit.play()
            not_hit = False
    for coin in actors.coins:
        if coin.y < 600:
            coin.y += 2
        else:
            coin.pos = randint(175, 625), randint(-800, -200)
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
        actors.current_screen = 'question_time'
        game_questions.question_screen = 'points'
    actors.moving(actors.swimmer, None)

#Drawing

actors = GameActors()
game_questions = GameQuestions()
#Game state variables

def draw():
    print(actors.current_screen)
    screen.clear()
    screen.blit("river", (0, 0))
    if actors.current_screen == 'start':
        actors.draw_start_screen()
    elif actors.current_screen == 'gamemode':
        actors.draw_gamemode_screen()
    elif actors.current_screen == 'difficulty_speed' or actors.current_screen == 'difficulty_points':
        actors.draw_difficulty_screen()
    elif actors.current_screen == 'speedrun_easy':
        actors.set_background(screen)
        actors.swimmer.draw()
        actors.q_block.draw()
        screen.draw.text("Time: " + str(game_clocks.count), color="orange red", topleft=(20,20), fontsize=40)
        actors.create_actors(actors.logs)
        actors.create_actors(actors.powerups)
    elif actors.current_screen == 'points_easy':
        actors.set_background(screen)
        actors.swimmer.draw()
        actors.q_block.draw()
        screen.draw.text("Time: " + str(game_clocks.count_down_max), color="orange red", topleft=(20,20), fontsize=40)
        screen.draw.text("Score: " + str(game_clocks.score), color="orange red", topleft=(670,20), fontsize=40)
        actors.create_actors(actors.logs)
        actors.create_actors(actors.coins)
    elif actors.current_screen == 'speedrun_medium':
        actors.set_background(screen)
        actors.swimmer.draw()
        screen.draw.text("Time: " + str(game_clocks.count), color="orange red", topleft=(20,20), fontsize=40)
    elif actors.current_screen == 'points_medium':
        actors.set_background(screen)
        actors.swimmer.draw()
        screen.draw.text("Time: " + str(game_clocks.count_down_max), color="orange red", topleft=(20,20), fontsize=40)
        screen.draw.text("Score: " + str(game_clocks.score), color="orange red", topleft=(670,20), fontsize=40)
    #Game over screens:
    elif actors.current_screen == 'gameover_speed':
        actors.set_background(screen)
        screen.draw.text("You completed the level in: " + str(game_clocks.count) + " seconds!", color="black", center=settings.CENTER, fontsize=60)
        actors.goback.draw()
    elif actors.current_screen == 'gameover_points':
        actors.set_background(screen)
        screen.draw.text("You ended with: " + str(game_clocks.score) + " points!", color="black", center=settings.CENTER, fontsize=60)
        actors.goback.draw()
    #Question screen
    elif actors.current_screen == 'question_time':
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
    global show_count, game_over_coin, question_time, score, count_max
    clicked_actor = actors.handle_mouse_down(pos)
    if clicked_actor == 'start' and actors.current_screen == "start":
        sounds.select.play()
        actors.current_screen = 'gamemode'
    elif clicked_actor == 'speedrun' and actors.current_screen == "gamemode":
        sounds.select.play()
        actors.current_screen = 'difficulty_speed'
    elif clicked_actor == 'pointsmania' and actors.current_screen == "gamemode":
        sounds.select.play()
        actors.current_screen = 'difficulty_points'
    elif clicked_actor == 'goback':
        sounds.goback.play()
        if actors.current_screen == 'gameover_speed' or actors.current_screen == 'gameover_points':
            music.play("loadscreen")
        game_clocks.reset_variables()
        actors.current_screen = 'start'
    elif clicked_actor == 'easy' and (actors.current_screen == 'difficulty_speed' or actors.current_screen == 'difficulty_points'):
        shuffle(game_questions.questions_e)
        if actors.current_screen == 'difficulty_speed':
            sounds.select.play()
            music.play("strength")
            actors.current_screen = 'speedrun_easy'
        elif actors.current_screen == 'difficulty_points':
            sounds.select.play()
            music.play("behemoth")
            actors.current_screen = 'points_easy'
    elif clicked_actor == 'medium' and (actors.current_screen == 'difficulty_speed' or actors.current_screen == 'difficulty_points'):
        if actors.current_screen == 'difficulty_speed':
            sounds.select.play()
            music.play("monster")
            actors.current_screen = 'speedrun_medium'
        elif actors.current_screen == 'difficulty_points':
            sounds.select.play()
            music.play("hero")
            actors.current_screen = 'points_medium'
    elif actors.current_screen == "question_time":
        for index, box in enumerate(game_questions.answer_boxes, start=1):
            print(f"Checking box {index} at position {pos}")
            if box.collidepoint(pos) and game_questions.question_screen == 'points':
                actors.current_screen, game_questions.answer = game_questions.update_game_state_points(index, sounds)
                game_questions.question_e = game_questions.questions_e.pop(0)
            elif box.collidepoint(pos) and game_questions.question_screen == 'speed':
                print(f"Box {index} clicked, updating game state")
                actors.current_screen, game_questions.answer = game_questions.update_game_state_speed(index, sounds)
                game_questions.question_e = game_questions.questions_e.pop(0)




def update():
    if actors.current_screen == 'start':
        if actors.number_of_updates == 15:
            actors.actors_image_change(actors.gamename, actors.game_name_states)
            actors.number_of_updates = 0
        else:
            actors.number_of_updates += 1
    elif actors.current_screen == 'gamemode':
        if actors.number_of_updates == 15:
            actors.actors_image_change(actors.gamemode, actors.gamemode_states)
            actors.number_of_updates = 0
        else:
            actors.number_of_updates += 1
    elif actors.current_screen == 'difficulty_speed' or actors.current_screen == 'difficulty_points':
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
    elif actors.current_screen == 'speedrun_easy':
        speedrun_level_easy()
        actors.moving_bg()
    elif actors.current_screen == 'points_easy':
        points_level_easy()
        actors.moving_bg()
    elif actors.current_screen == 'speedrun_medium':
        actors.moving_bg()
    elif actors.current_screen == 'points_medium':
        actors.moving_bg()
    #Question interactions








pgzrun.go()
