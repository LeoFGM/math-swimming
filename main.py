import threading
import time
import pgzrun
import pygame

from pgzero.builtins import keys

from game import (GameActors, ActorMovementInteractions, AnimationManager, CompActors, GameClocks,
                  speedrun_level_easy, points_level_easy, speedrun_level_medium, points_level_medium,
                  GameQuestions, Screen, MenuScreens, GameScreens, GameOverScreens, QuestionScreens, TransitionManager, settings, MusicalActions)
from constants import GameState, QuestionStates

#Initialize pygame and main music

pygame.init()
music.set_volume(0.25)
music.play("loadscreen")



#Initialize game components
game_clocks = GameClocks()
game_actors = GameActors()
actor_animation = AnimationManager(game_actors)
comp_actors = CompActors(game_actors)
game_questions = GameQuestions()
music_actions = MusicalActions()
current_screen = GameState.START
menu_screens = MenuScreens(game_actors)
game_screens = GameScreens(game_actors)
actor_movement = ActorMovementInteractions(actor_animation, game_screens.transition_manager)
game_over_screens = GameOverScreens(game_actors)
actor_animation.set_background_manager(actor_movement.background_manager)


#Resetting game state function
def reset_game_state():
    global current_screen
    sounds.goback.play()
    music.play("loadscreen")
    game_clocks.reset_variables()
    game_actors.x = 250
    actor_movement.scroll = 0
    game_actors.reset_all_actors()
    game_actors.show_level_selection_actors()

#Handle question logic

def handle_question_screen(pos):
    global current_screen

    for index, box in enumerate(game_questions.answer_boxes, start=0):
        if box.collidepoint(pos):
            question_screen_map = {
                QuestionStates.POINTS_EASY: lambda: game_questions.update_question_state(index, game_questions.question_e, sounds,
                                                                               GameState.POINTS_EASY),
                QuestionStates.SPEED_EASY: lambda: game_questions.update_question_state(index, game_questions.question_e, sounds,
                                                                             GameState.SPEEDRUN_EASY),
                QuestionStates.POINTS_MEDIUM: lambda: game_questions.update_question_state(index, game_questions.question_m, sounds,
                                                                               GameState.POINTS_MEDIUM),
                QuestionStates.SPEED_MEDIUM: lambda: game_questions.update_question_state(index, game_questions.question_m,
                                                                              sounds, GameState.SPEEDRUN_MEDIUM)
            }
            if game_questions.question_screen in question_screen_map:
                current_screen, game_questions.answer = question_screen_map[game_questions.question_screen]()
                game_questions.analyze_answer(game_clocks)
                game_questions.get_first_question(current_screen)
        else:
            print(f"Answer box {index} not clicked")

#Drawing game function

def draw():
    screen.clear()
    screen.blit("river", (0, 0))

    # Check both transition managers

    if not (menu_screens.transition_manager.transition_active or
    menu_screens.transition_manager.flash_active or
    game_screens.transition_manager.transition_active or
    game_screens.transition_manager.flash_active):

        screen_actions = {
            GameState.START: lambda : MenuScreens(game_actors).draw_start_screen(screen),
            GameState.GAMEMODE: lambda : MenuScreens(game_actors).draw_gamemode_screen(screen),
            GameState.DIFFICULTY_SPEED: lambda : MenuScreens(game_actors).draw_difficulty_screen(screen),
            GameState.DIFFICULTY_POINTS: lambda : MenuScreens(game_actors).draw_difficulty_screen(screen),
            GameState.SPEEDRUN_EASY: lambda : GameScreens(game_actors).draw_speedrun_easy_screen(screen, game_clocks, game_actors, actor_movement, actor_animation),
            GameState.POINTS_EASY: lambda : GameScreens(game_actors).draw_points_easy_screen(screen, game_clocks, game_actors, actor_movement, actor_animation),
            GameState.SPEEDRUN_MEDIUM: lambda : GameScreens(game_actors).draw_speedrun_medium_screen(screen, game_clocks, game_actors, actor_movement, actor_animation),
            GameState.POINTS_MEDIUM: lambda : GameScreens(game_actors).draw_points_medium_screen(screen, game_clocks, game_actors, actor_movement, actor_animation, comp_actors),
            GameState.GAMEOVER_SPEED: lambda : GameOverScreens(game_actors).draw_gameover_speed_screen(screen, settings, game_clocks, game_actors),
            GameState.GAMEOVER_POINTS: lambda : GameOverScreens(game_actors).draw_gameover_points_screen(screen, settings, game_clocks, game_actors),
            GameState.QUESTION_TIME: lambda : QuestionScreens().draw_question_screen(screen, game_questions)
        }
        if current_screen in screen_actions:
            screen_actions[current_screen]()

    active_transition = None
    if menu_screens.transition_manager.transition_active or menu_screens.transition_manager.flash_active:
        active_transition = menu_screens.transition_manager
    elif game_screens.transition_manager.transition_active or game_screens.transition_manager.flash_active:
        active_transition = game_screens.transition_manager

    if active_transition:
        active_transition.draw(screen)


#Handling mouse clicks function

def on_mouse_down(pos):
    global current_screen
    clicked_actor = game_actors.handle_mouse_down(pos)
    if not clicked_actor:
        if current_screen == GameState.QUESTION_TIME:
            pass
        else:
            return


    screen_transitions = {
        'start': GameState.GAMEMODE,
        'speedrun': GameState.DIFFICULTY_SPEED,
        'pointsmania': GameState.DIFFICULTY_POINTS,
        'goback': GameState.START,
    }

    difficulty_transitions = {
        'easy': {GameState.DIFFICULTY_SPEED: GameState.SPEEDRUN_EASY, GameState.DIFFICULTY_POINTS: GameState.POINTS_EASY},
        'medium': {GameState.DIFFICULTY_SPEED: GameState.SPEEDRUN_MEDIUM, GameState.DIFFICULTY_POINTS: GameState.POINTS_MEDIUM}
    }

    if clicked_actor in screen_transitions:
        if clicked_actor == 'goback' and (current_screen == GameState.GAMEOVER_SPEED or current_screen == GameState.GAMEOVER_POINTS):
            reset_game_state()
        target_screen = screen_transitions[clicked_actor]
        menu_screens.transition_manager.current_screen = current_screen
        menu_screens.transition_manager.start_transition(target_screen)
        sounds.select.play()


    elif clicked_actor in difficulty_transitions:
        sounds.select.play()
        if current_screen in difficulty_transitions[clicked_actor]:
            target_screen = difficulty_transitions[clicked_actor][current_screen]

            music.stop()

            game_screens.transition_manager.start_transition(target_screen)
            game_actors.hide_level_selection_actors()
            game_questions.get_first_question(target_screen)
            game_clocks.start_level_timer()

            def play_new_music():
                time.sleep(0.5)
                if target_screen.value in music_actions.music_list:
                    music.play(music_actions.music_list[target_screen.value])
            threading.Thread(target=play_new_music).start()
        else:
            print(f"Error: '{current_screen}' not found in {difficulty_transitions[clicked_actor]}")

        if current_screen.value in music_actions.music_list:
            music.stop()
            music.play(music_actions.music_list[current_screen.value])

    elif current_screen == GameState.QUESTION_TIME:
        handle_question_screen(pos)


    else:
        print(f"Unhandled screen: {current_screen}")  # Debugging


def on_key_down(key):
    global current_screen
    if key == keys.SPACE and game_actors.push_powerup_active and current_screen not in [GameState.START, GameState.GAMEMODE, GameState.DIFFICULTY_POINTS, GameState.DIFFICULTY_SPEED]:
        nearest_log = None
        min_distance = float("inf")
        sounds.punch.play()

        for log in game_actors.logs:

            if hasattr(log, 'is_being_pushed') and log.is_being_pushed:
                continue

            distance = ((game_actors.swimmer.x - log.x) ** 2 +
                        (game_actors.swimmer.y - log.y) ** 2) ** 0.5

            if distance < 150 and distance < min_distance:
                nearest_log = log
                min_distance = distance

        if nearest_log:
            nearest_log.is_being_pushed = True
            nearest_log.push_start_time = time.time()
            nearest_log.original_pos = (nearest_log.x, nearest_log.y)







def update(dt):
    global current_screen

    menu_result = menu_screens.transition_manager.update(1 / 60)
    game_result = game_screens.transition_manager.update(1 / 60)
    game_clocks.update_timers(dt)


    if menu_result:
        current_screen = menu_result
    elif game_result:
        current_screen = game_result

    update_actions = {
        GameState.START: lambda: menu_screens.update_static_screen(actor_animation, actor_movement, current_screen),
        GameState.GAMEMODE: lambda: menu_screens.update_static_screen(actor_animation, actor_movement, current_screen),
        GameState.DIFFICULTY_SPEED: lambda: menu_screens.update_static_screen(actor_animation, actor_movement, current_screen),
        GameState.DIFFICULTY_POINTS: lambda: menu_screens.update_static_screen(actor_animation, actor_movement, current_screen),
        GameState.SPEEDRUN_EASY: lambda: game_screens.update_game_screen(GameState.SPEEDRUN_EASY, actor_movement, speedrun_level_easy, game_clocks,
                                                            game_actors, actor_movement, actor_animation,
                                                            game_questions, current_screen, game_screens, music_actions, sounds),
        GameState.POINTS_EASY: lambda: game_screens.update_game_screen(GameState.POINTS_EASY, actor_movement, points_level_easy, game_clocks,
                                                          game_actors, actor_movement, actor_animation, game_questions,
                                                          current_screen, game_screens, sounds),
        GameState.SPEEDRUN_MEDIUM: lambda: game_screens.update_game_screen(GameState.SPEEDRUN_MEDIUM, actor_movement, speedrun_level_medium,
                                                              game_clocks, game_actors, actor_movement, actor_animation,
                                                              game_questions, current_screen,  game_screens, music_actions, sounds, dt),
        GameState.POINTS_MEDIUM: lambda: game_screens.update_game_screen(GameState.POINTS_MEDIUM, actor_movement, points_level_medium, game_clocks, game_actors,
                                                            comp_actors, actor_movement, actor_animation, game_questions, current_screen, game_screens, sounds, dt),
        GameState.GAMEOVER_SPEED: lambda: current_screen,
        GameState.GAMEOVER_POINTS: lambda: current_screen,
        GameState.QUESTION_TIME: lambda: current_screen,
    }

    if current_screen in update_actions:
        current_screen = update_actions[current_screen]()

pgzrun.go()