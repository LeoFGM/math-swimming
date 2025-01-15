import pgzrun
from random import randint
from screen import *
from actors import GameActors
from settings import settings

from changevar import *
from animations import *
from utils import *
from questions import *

import time
import math

#Clocks

def countup():
    global count, show_count, game_over_speed, count_max, speed_easy_screen, action1
    if count < count_max:
        count += 1
        clock.schedule(countup, 1)
    else:
        show_count = False
        speed_easy_screen = False
        game_over_speed = True
    return


def countdown():
    global count_down_max, show_count, points_easy_screen, game_over_coin
    if count_down_max > 0:
        count_down_max -= 1
        clock.schedule(countdown, 1)
    else:
        show_count = False
        points_easy_screen = False
        game_over_coin = True
    return

#Variables reset

def reset_variables():
    global count, count_max, action, action1, count_down_max
    count = 0
    count_max = 60
    count_down_max = 60
    action = 0
    action1 = 0
    return

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
    hit_animation = False
    not_hit = True

action_1 = 0
action_2 = 0

def speedrun_level_easy():
    global action_2, show_count, action1, count_max, speed_easy_screen, speed_question_e, question_time
    global last_collision, not_hit, hit_animation, powerup, powerup_collision, hit_updates
    global logs_already_created, powerups_already_created
    if not question_time:
        if action_2 == 0:
            if not logs_already_created:
                for i in range(0, 3):
                    new_log()
                    logs_already_created = True
            if not powerups_already_created:
                for i in range(0, 1):
                    new_power_up()
                powerups_already_created = True
        action_2 = 1
        index_lists(logs)
        show_count = True
        ts = time.time()
        if show_count and action1 == 0:
            countup()
            action1 = 1
            for log in logs:
                log.y = randint(-800, -300)
        if not_hit or not powerup_collision:
            not_hit_swimmer()
        elif powerup_collision and not_hit:
            pu_swimmer()
        for log in logs:
            if log.y < 600 and not powerup_collision:
                log.y += 2
            elif log.y < 600 and powerup_collision:
                log.y += 3
            else:
                log.y = randint(-800, -500)
            log_animation(log)
            if (swimmer.colliderect(log)) and (ts - last_collision >= 3):
                count_max += 3
                last_collision = ts
                sounds.hit.play()
                not_hit = False
                hit_animation = True
        for powerup in powerups:
            if powerup.y < 600 and not powerup_collision:
                powerup.y += 2
            elif powerup.y < 0 and powerup_collision:
                powerup.y = randint(-800, -500)
            else:
                powerup.y = randint(-800, -500)
            powerups_animation(powerup)
            for log in logs:
                if powerup.colliderect(log):
                    powerup.y += 75
                if q_block.colliderect(log):
                    log.y += 100
                if q_block.colliderect(powerup):
                    powerup.y += 75
            if swimmer.colliderect(powerup):
                powerup_collision = True
                count_max -= 5
                music.stop()
                music.play("stasis")
                music.fadeout(5)
                clock.schedule(stop_powerup, 5)
                clock.schedule(change_music, 5)
        if q_block.y < 600:
            q_block.y += 2
        else:
            q_block.y = randint(-2000, -1600)
        if swimmer.colliderect(q_block):
            q_block.y = randint(-2000, -1600)
            speed_easy_screen = False
            speed_question_e = True
            question_time = True
        if hit_animation:
            if hit_updates == 6:
                actors_animation(swimmer, swimmer_states_hit)
                hit_updates = 0
            else:
                hit_updates += 1
            clock.schedule(stop_swimmer_hit_animation, 3)
        moving(speed_easy_screen, powerup_collision)

def points_level_easy():
    global action, action_1, show_count, score, number_of_updates_log, last_collision, hit_animation, hit_updates, number_of_updates_coin
    global points_easy_screen, not_hit, number_of_updates_swimmer, logs_already_created, coins_already_created, question_time, point_question_e
    if not question_time:
        if action_1 == 0:
            if not logs_already_created:
                for i in range(0, 3):
                    new_log()
                logs_already_created = True
            if not coins_already_created:
                for i in range(0, 20):
                    new_coin()
                coins_already_created = True
        action_1 = 1
        index_lists(logs)
        show_count = True
        ts = time.time()
        if show_count and action == 0:
            countdown()
            action = 1
            for log in logs:
                log.y = randint(-800, -300)
        if not_hit:
            not_hit_swimmer()
        for log in logs:
            if log.y < 600:
                log.y += 2
            else:
                log.y = randint(-800, -500)
            log_animation(log)
            if (swimmer.colliderect(log)) and (ts - last_collision >= 3):
                score -= 3
                last_collision = ts
                sounds.hit.play()
                not_hit = False
                hit_animation = True
        for coin in coins:
            if coin.y < 600:
                coin.y += 2
            else:
                coin.pos = randint(175, 625), randint(-800, -200)
            for log in logs:
                if coin.colliderect(log):
                    coin.y += 30
                if q_block.colliderect(log) and q_block.y:
                    log.y += 100
                if q_block.colliderect(coin) and q_block.y:
                    coin.y += 75
            coin_animation(coin)
            if swimmer.colliderect(coin):
                score += 1
                sounds.coin.play()
                coin.pos = randint(175, 625), randint(-800, -200)
        if q_block.y < 600:
            q_block.y += 2
        else:
            q_block.y = randint(-2000, -1600)
        if swimmer.colliderect(q_block):
            q_block.y = randint(-2000, -1600)
            points_easy_screen = False
            point_question_e = True
            question_time = True
        if hit_animation:
            if hit_updates == 6:
                actors_animation(swimmer, swimmer_states_hit)
                hit_updates = 0
            else:
                hit_updates += 1
            clock.schedule(stop_swimmer_hit_animation, 3)
        moving(points_easy_screen, None)

#Drawing

actors = GameActors()

#Game state variables
current_screen = 'start'

def draw():
    screen.clear()
    screen.blit("river", (0, 0))
    if current_screen == 'start':
        actors.draw_start_screen()
    elif current_screen == 'gamemode':
        actors.draw_gamemode_screen()
    elif current_screen == 'difficulty':
        actors.draw_difficulty_screen()
    #Speed mode screens
    elif current_screen == 'speedrun':
        actors.set_background(screen)
        actors.display_diff()
        actors.goback.draw()
    elif current_screen == 'speedrun_easy':
        actors.set_background(screen)
        actors.swimmer.draw()
        screen.draw.text("Time: " + str(count), color="orange red", topleft=(30, 30), fontsize=40)
        for log in actors.logs:
            log.draw()
        for powerup in actors.powerups:
            if not powerup_collision:
                powerup.draw()
    #Points mode screens
    elif current_screen == 'pointsmania':
        actors.set_background(screen)
        actors.display_diff()
        actors.goback.draw()
    elif current_screen == 'points_easy':
        actors.set_background(screen)
        actors.swimmer.draw()
        screen.draw.text("Time: " + str(count_down_max), color="orange red", topleft=(30, 30), fontsize=40)
        screen.draw.text("Score:  " + str(score), color="orange red", topleft=(660, 30), fontsize=40)
        for log in actors.logs:
            log.draw()
        for coin in actors.coins:
            coin.draw()
    #Game over screens:
    if game_over_speed:
        set_background(screen)
        screen.draw.text("You completed the level in: " + str(count) + " seconds!", color="black", center=settings.CENTER, fontsize=60)

    if game_over_coin:
        set_background(screen)
        screen.draw.text("You ended with: " + str(score) + " points!", color="black", center=settings.CENTER, fontsize=60)

    #Question screen
    if question_time:
        set_background(screen)
        screen.draw.filled_rect(main_box, "sky blue")
        screen.draw.filled_rect(timer_box, "sky blue")
        for box in answer_boxes:
            screen.draw.filled_rect(box, "medium slate blue")
        screen.draw.textbox(str(time_left_e), timer_box, color="black")
        screen.draw.textbox(question_e[0], main_box, color="black")
        index = 1
        for box in answer_boxes:
            screen.draw.textbox(question_e[index], box, color="black")
            index = index + 1






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
    elif current_screen == 'speedrun' or current_screen == 'pointsmania':
        if actors.number_of_updates == 3:
            actors.difficulties_animation()
            actors.number_of_updates = 0
        else:
            actors.number_of_updates += 1
    elif current_screen == 'speedrun_easy':
        speedrun_level_easy()
        actors.moving_bg()
    elif current_screen == 'points_easy':
        points_level_easy()
        actors.moving_bg()






def speed_screen(sounding, musical):
    if speedscreen:
        sounding.select.play()
        musical.stop()
        musical.play("strength")
        return True

def points_screen(sounding, musical):
    global pointscreen
    if pointscreen:
        sounding.select.play()
        musical.stop()
        pointscreen = False
        musical.play("behemoth")
        return True




def on_mouse_down(pos):
    global screen1, screen2, speedscreen, pointscreen, speed_easy_screen, game_over_speed, point_question_e, speed_question_e
    global show_count, points_easy_screen, game_over_coin, question_time, score, count_max
    global current_screen
    clicked_actor = actors.handle_mouse_down(pos)
    if clicked_actor == 'start':
        sounds.select.play()
        current_screen = 'gamemode'
    elif clicked_actor == 'speedrun':
        sounds.select.play()
        current_screen = 'difficulty'
    elif clicked_actor == 'pointsmania':
        sounds.select.play()
        current_screen = 'difficulty'
    elif clicked_actor == "goback":
        sounds.goback.play()
        current_screen = 'start'
    elif current_screen == 'speedrun' and clicked_actor == 'easy':
        sounds.select.play()
        current_screen = 'speedrun_easy'
    elif current_screen == 'pointmania' and clicked_actor == 'easy':
        sounds.select.play()
        current_screen = 'points_easy'

    #Question interactions
    if question_time:
        index = 1
        for box in answer_boxes:
            if box.collidepoint(pos) and point_question_e:
                points_easy_screen, question_time, point_question_e = update_game_state_points(index, question_e, point_question_e, sounds)
            elif box.collidepoint(pos) and speed_question_e:
                speed_easy_screen, question_time, speed_question_e = update_game_state_speed(index, question_e, speed_question_e, sounds)
            index = index + 1


pgzrun.go()
