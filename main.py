import pgzrun
import pygame

from game import (GameActors, ActorMovementInteractions, AnimationManager, CompActors, GameClocks,
                  speedrun_level_easy, points_level_easy, speedrun_level_medium, points_level_medium,
                  GameQuestions, MenuScreens, GameScreens, GameOverScreens, QuestionScreens, settings, MusicalActions)

pygame.init()

music.set_volume(0.25)
music.play("loadscreen")

game_clocks = GameClocks()
game_actors = GameActors()
actor_animation = AnimationManager(game_actors)
actor_movement = ActorMovementInteractions(actor_animation)
comp_actors = CompActors(game_actors)
game_questions = GameQuestions()
music_actions = MusicalActions()
current_screen = 'start'

#Game state variables


def draw():
    screen.clear()
    screen.blit("river", (0, 0))
    screen_actions = {
        'start': lambda : MenuScreens.draw_start_screen(None, game_actors),
        'gamemode': lambda : MenuScreens.draw_gamemode_screen(None, game_actors),
        'difficulty_speed': lambda : MenuScreens.draw_difficulty_screen(None, game_actors),
        'difficulty_points': lambda : MenuScreens.draw_difficulty_screen(None, game_actors),
        'speedrun_easy': lambda : GameScreens.draw_speedrun_easy_screen(None, screen, game_clocks, game_actors, actor_movement),
        'points_easy': lambda : GameScreens.draw_points_easy_screen(None, screen, game_clocks, game_actors, actor_movement),
        'speedrun_medium': lambda : GameScreens.draw_speedrun_medium_screen(None, screen, game_clocks, game_actors, actor_movement),
        'points_medium': lambda : GameScreens.draw_points_medium_screen(None, screen, game_clocks, game_actors, actor_movement, comp_actors),
        'gameover_speed': lambda : GameOverScreens.draw_gameover_speed_screen(None, screen, settings, game_clocks, game_actors),
        'gameover_points': lambda : GameOverScreens.draw_gameover_points_screen(None, screen, settings, game_clocks, game_actors),
        'question_time': lambda : QuestionScreens.draw_question_screen(None, screen, game_questions)
    }
    if current_screen in screen_actions:
        screen_actions[current_screen]()




def on_mouse_down(pos):
    global current_screen

    def reset_game_state():
        sounds.goback.play()
        if current_screen in ['gameover_speed', 'gameover_points']:
            music.play("loadscreen")
        game_clocks.reset_variables()
        game_actors.x = 250
        actor_movement.scroll = 0
        game_actors.reset_all_actors()
        actor_movement.backgrounds.clear()
        game_actors.show_level_selection_actors()

    def handle_difficulty(actor_clicked, difficulties):
        for key, value in difficulties.items():
            if key == current_screen:
                print(f"Before condition: Current screen = '{current_screen}'")
                sounds.select.play()
                return difficulties[current_screen]
        else:
            print(f"Warning: Actor '{actor_clicked}' not found in difficulties.")
            return current_screen

    print(f"Current screen: '{current_screen}'")
    print(f"Music list keys: {list(music_actions.music_list.keys())}")


    clicked_actor = game_actors.handle_mouse_down(pos)
    print(f"Clicked actor: {clicked_actor}")

    screen_transitions = {
        'start': lambda: 'gamemode' if current_screen == 'start' else None,
        'speedrun': lambda: 'difficulty_speed' if current_screen == 'gamemode' else None,
        'pointsmania': lambda: 'difficulty_points' if current_screen == 'gamemode' else None,
        'goback': reset_game_state,
    }

    difficulty_transitions = {
        'easy': {'difficulty_speed': 'speedrun_easy', 'difficulty_points': 'points_easy'},
        'medium': {'difficulty_speed': 'speedrun_medium', 'difficulty_points': 'points_medium'}
    }

    if clicked_actor in screen_transitions:
        new_screen = screen_transitions[clicked_actor]()
        if new_screen:
            sounds.select.play()
            current_screen = new_screen
        elif clicked_actor == 'pointsmania' or clicked_actor == 'speedrun':
            pass
        elif clicked_actor == 'goback':
            current_screen = 'start'

    elif clicked_actor in difficulty_transitions:

        if current_screen in difficulty_transitions[clicked_actor]:
            print(f"Transitioning to: {difficulty_transitions[clicked_actor][current_screen]}")
            current_screen = handle_difficulty(
                clicked_actor, difficulty_transitions[clicked_actor]
            )
            game_actors.hide_level_selection_actors()
            game_questions.get_first_question(current_screen)
            if current_screen in music_actions.music_list:
                print(f"Playing: {music_actions.music_list[current_screen]}")
                music.stop()
                music.play(music_actions.music_list[current_screen])
        else:
            print(f"Error: '{current_screen}' not found in {difficulty_transitions[clicked_actor]}")

    elif current_screen == "question_time":
        handle_question_screen(pos)

    print(game_actors.start.pos)


def handle_question_screen(pos):
    global current_screen

    for index, box in enumerate(game_questions.answer_boxes, start=0):
        if box.collidepoint(pos):
            print(current_screen)
            print(f"Checking box {index} at position {pos}")
            question_screen_map = {
                'points_easy': lambda: game_questions.update_question_state(index, game_questions.question_e, sounds,
                                                                               'points_easy'),
                'speed_easy': lambda: game_questions.update_question_state(index, game_questions.question_e, sounds,
                                                                             'speedrun_easy'),
                'speed_medium': lambda: game_questions.update_question_state(index, game_questions.question_m, sounds,
                                                                               'speedrun_medium'),
                'points_medium': lambda: game_questions.update_question_state(index, game_questions.question_m,
                                                                              sounds, 'points_medium')
            }

            if game_questions.question_screen in question_screen_map:
                current_screen, game_questions.answer = question_screen_map[game_questions.question_screen]()
                game_questions.analyze_answer(game_clocks)
                game_questions.get_first_question(current_screen)



def update():
    global current_screen
    if current_screen == 'difficulty_speed' or current_screen == 'difficulty_points' or current_screen == 'start' or current_screen == 'gamemode':
        actor_animation.static_update_animations()
        actor_movement.scroll = 0
    elif current_screen == 'speedrun_easy':
        current_screen = speedrun_level_easy(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, music_actions, sounds)
        actor_movement.moving_bg()
    elif current_screen == 'points_easy':
        current_screen = points_level_easy(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, sounds)
        actor_movement.moving_bg()
    elif current_screen == 'speedrun_medium':
        actor_movement.moving_bg()
        current_screen = speedrun_level_medium(game_clocks, game_actors, actor_movement, actor_animation, game_questions, current_screen, music_actions, sounds)
    elif current_screen == 'points_medium':
        actor_movement.moving_bg()
        current_screen = points_level_medium(game_clocks, game_actors, comp_actors, actor_movement, actor_animation, game_questions, current_screen, sounds)


pgzrun.go()