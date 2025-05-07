import threading
import time
import pgzrun
import pygame

from pgzero.builtins import keys

#Core systems
from game.core.context import GameContext
from game.core.clock import GameClocks
from game.core.audio import MusicalActions
from game.core import settings

#Actors
from game.actors import (GameActors, AnimationManager, CompActors, ActorMovementInteractions)

#Gameplay
from game.gameplay.questions.question_actions import GameQuestions
from game.gameplay.levels import (speedrun_level_easy, points_level_easy, speedrun_level_medium, points_level_medium)

#Screens
from game.screens import (MenuScreens, GameScreens, QuestionScreens, GameOverScreens)

#Constants
from game.constants import GameState
from game.screens.transitions import TransitionManager

#Initialize pygame and main music

pygame.init()
music.set_volume(0.25)
music.play("loadscreen")



#Initialize game components
shared_transition_manager = TransitionManager()
context = GameContext()
context.inject_dependencies(clock=GameClocks(), actors=GameActors(), audio=MusicalActions(), questions=GameQuestions(), transitions=shared_transition_manager, sounds=sounds)

context.animation = AnimationManager(context.actors)
context.comp_actors = CompActors(context.actors, context.transitions)
context.current_screen = GameState.START

context.screens = {'menu': MenuScreens(context.actors),
                   'game': GameScreens(context.actors, shared_transition_manager),
                   'gameover': GameOverScreens(context.actors),
                   'questions': QuestionScreens()
}
context.movement = ActorMovementInteractions(context.animation, context.transitions)
context.animation.set_background_manager(context.movement.background_manager)

#Resetting game state function
def reset_game_state():
    sounds.goback.play()
    music.play("loadscreen")
    context.clock.reset_variables()
    context.actors.x = 250
    context.movement.scroll = 0
    context.actors.reset_all_actors()
    context.actors.show_level_selection_actors()




#Drawing game function

def draw():
    screen.clear()
    screen.blit("river", (0, 0))

    # Transition checking

    if not (context.screens['menu'].transition_manager.transition_active or
    context.screens['menu'].transition_manager.flash_active or
    context.screens['game'].transition_manager.transition_active or
    context.screens['game'].transition_manager.flash_active or context.screens['game'].transition_manager.powerup_message_active):

    #Screen drawing dict
        screen_actions = {
            GameState.START: lambda : context.screens['menu'].draw_start_screen(screen), #The screen (GameState), then its respective drawing method
            GameState.GAMEMODE: lambda : context.screens['menu'].draw_gamemode_screen(screen),
            GameState.DIFFICULTY_SPEED: lambda : context.screens['menu'].draw_difficulty_screen(screen),
            GameState.DIFFICULTY_POINTS: lambda : context.screens['menu'].draw_difficulty_screen(screen),
            GameState.SPEEDRUN_EASY: lambda : context.screens['game'].draw_speedrun_easy_screen(screen, context),
            GameState.POINTS_EASY: lambda : context.screens['game'].draw_points_easy_screen(screen, context),
            GameState.SPEEDRUN_MEDIUM: lambda : context.screens['game'].draw_speedrun_medium_screen(screen, context),
            GameState.POINTS_MEDIUM: lambda : context.screens['game'].draw_points_medium_screen(screen, context),
            GameState.GAMEOVER_SPEED: lambda : context.screens['gameover'].draw_gameover_speed_screen(screen, settings, context),
            GameState.GAMEOVER_POINTS: lambda : context.screens['gameover'].draw_gameover_points_screen(screen, settings, context),
            GameState.QUESTION_TIME: lambda : context.screens['questions'].draw_question_screen(screen, context)
        }
        if context.current_screen in screen_actions:
            screen_actions[context.current_screen]()

    #Transition executor
    active_transition = None
    if context.screens['menu'].transition_manager.transition_active or context.screens['menu'].transition_manager.flash_active:
        active_transition = context.screens['menu'].transition_manager
    elif context.screens['game'].transition_manager.transition_active or context.screens['game'].transition_manager.flash_active or context.screens['game'].transition_manager.powerup_message_active:
        active_transition = context.screens['game'].transition_manager


    if active_transition:
        active_transition.draw(screen)


#Handling mouse clicks function

def on_mouse_down(pos):
    #Method that checks collisions like the easy button and more
    clicked_actor = context.actors.handle_mouse_down(pos)

    if not clicked_actor:
        if context.current_screen == GameState.QUESTION_TIME:
            pass
        else:
            return

    #Depending on the current_screen (key) the screen will transition into a new one (value)
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
    #Executor of the screen transitions
    if clicked_actor in screen_transitions:
        if clicked_actor == 'goback' and (context.current_screen == GameState.GAMEOVER_SPEED or context.current_screen == GameState.GAMEOVER_POINTS):
            reset_game_state()
        target_screen = screen_transitions[clicked_actor]
        context.screens['menu'].transition_manager.current_screen = context.current_screen #Makes the transitioning
        context.screens['menu'].transition_manager.start_transition(target_screen) #Makes the transitioning
        sounds.select.play()


    elif clicked_actor in difficulty_transitions:
        sounds.select.play()
        if context.current_screen in difficulty_transitions[clicked_actor]:
            target_screen = difficulty_transitions[clicked_actor][context.current_screen]

            music.stop()
            context.questions.get_first_question(target_screen)

            context.screens['game'].transition_manager.start_transition(target_screen) #Makes the transitioning
            context.actors.hide_level_selection_actors()
            context.clock.start_level_timer()

            def play_new_music(): #Function to change music
                time.sleep(0.5)
                if target_screen.value in context.audio.music_list:
                    music.play(context.audio.music_list[target_screen.value])

            threading.Thread(target=play_new_music).start()
        else:
            print(f"Error: '{context.current_screen}' not found in {difficulty_transitions[clicked_actor]}")

        if context.current_screen.value in context.audio.music_list:
            music.stop()
            music.play(context.audio.music_list[context.current_screen.value])

    elif context.current_screen == GameState.QUESTION_TIME: #Question screen handler
         context.screens["questions"].handle_question_screen(context, pos, sounds)


    else:
        print(f"Unhandled screen: {context.current_screen}")  # Debugging


def on_key_down(key):
    #Pushing logs logic
    if key == keys.SPACE and context.actors.push_powerup_active and context.current_screen not in [GameState.START, GameState.GAMEMODE, GameState.DIFFICULTY_POINTS, GameState.DIFFICULTY_SPEED]:
        nearest_log = None
        min_distance = float("inf") #Checks nearest logs
        sounds.punch.play()

        for log in context.actors.logs:

            if hasattr(log, 'is_being_pushed') and log.is_being_pushed:
                continue #Checks if the log is already in the air pushed

            distance = ((context.player.x - log.x) ** 2 +
                        (context.player.y - log.y) ** 2) ** 0.5

            if distance < 150 and distance < min_distance:
                nearest_log = log
                min_distance = distance

        if nearest_log: #Changes logs position and does the parabola movement
            nearest_log.is_being_pushed = True
            nearest_log.push_start_time = time.time()
            nearest_log.original_pos = (nearest_log.x, nearest_log.y)



def update(dt):

    menu_result = context.screens['menu'].transition_manager.update(1 / 60) #Updates the transitions
    game_result = context.screens['game'].transition_manager.update(1 / 60) #Updates the transitions

    if context.current_screen == GameState.QUESTION_TIME: #Block of code that checks gets called if the question timer reached zero before answering
        def timeout_callback():
            new_screen = context.questions.on_timeout(context, sounds)
            context.current_screen = new_screen

        context.clock.update_timers(dt, timeout_callback)
    else:
        context.clock.update_timers(dt)

    #Map of all levels made, GameState (key), its method (value)
    update_actions = {
        GameState.START: lambda: context.screens['menu'].update_static_screen(context.animation, context.movement, context.current_screen),
        GameState.GAMEMODE: lambda: context.screens['menu'].update_static_screen(context.animation, context.movement, context.current_screen),
        GameState.DIFFICULTY_SPEED: lambda: context.screens['menu'].update_static_screen(context.animation, context.movement, context.current_screen),
        GameState.DIFFICULTY_POINTS: lambda: context.screens['menu'].update_static_screen(context.animation, context.movement, context.current_screen),
        GameState.SPEEDRUN_EASY: lambda: context.screens['game'].update_game_screen(GameState.SPEEDRUN_EASY, context, speedrun_level_easy, context),
        GameState.POINTS_EASY: lambda: context.screens['game'].update_game_screen(GameState.POINTS_EASY, context, points_level_easy, context),
        GameState.SPEEDRUN_MEDIUM: lambda: context.screens['game'].update_game_screen(GameState.SPEEDRUN_MEDIUM, context, speedrun_level_medium, context, dt),
        GameState.POINTS_MEDIUM: lambda: context.screens['game'].update_game_screen(GameState.POINTS_MEDIUM, context, points_level_medium, context, dt),
        GameState.GAMEOVER_SPEED: lambda: context.current_screen,
        GameState.GAMEOVER_POINTS: lambda: context.current_screen,
        GameState.QUESTION_TIME: lambda: context.current_screen,
    }

    if menu_result:
        context.current_screen = menu_result
    elif game_result:
        context.current_screen = game_result
    elif context.current_screen in update_actions and not game_result:
        context.current_screen = update_actions[context.current_screen]()


pgzrun.go()