import random
import pygame
import pgzrun

from levels import *

from utils import *
from questions import *

import time
import musicals

pygame.init()

music.set_volume(0.25)
music.play("loadscreen")

game_clocks = GameClocks()
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
    global current_screen
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
        current_screen = speedrun_level_easy(game_clocks, actors, game_questions, current_screen, sounds)
        actors.moving_bg()
    elif current_screen == 'points_easy':
        current_screen = points_level_easy(game_clocks, actors, game_questions, current_screen, sounds)
        actors.moving_bg()
    elif current_screen == 'speedrun_medium':
        actors.moving_bg()
        current_screen = speedrun_level_medium(game_clocks, actors, game_questions, current_screen, sounds)
    elif current_screen == 'points_medium':
        actors.moving_bg()
    #Question interactions








pgzrun.go()
