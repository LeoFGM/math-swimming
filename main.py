import pgzrun

from actors import GameActors
from changevar import GameClocks
from levels import *
from questions import *
from screens import MenuScreens, GameScreens, GameOverScreens, QuestionScreens
from settings import settings

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
    screen_actions = {
        'start': lambda : MenuScreens.draw_start_screen(None, actors),
        'gamemode': lambda : MenuScreens.draw_gamemode_screen(None, actors),
        'difficulty_speed': lambda : MenuScreens.draw_difficulty_screen(None, actors),
        'difficulty_points': lambda : MenuScreens.draw_difficulty_screen(None, actors),
        'speedrun_easy': lambda : GameScreens.draw_speedrun_easy_screen(None, screen, game_clocks, actors),
        'points_easy': lambda : GameScreens.draw_points_easy_screen(None, screen, game_clocks, actors),
        'speedrun_medium': lambda : GameScreens.draw_speedrun_medium_screen(None, screen, game_clocks, actors),
        'points_medium': lambda : GameScreens.draw_points_medium_screen(None, screen, game_clocks, actors),
        'gameover_speed': lambda : GameOverScreens.draw_gameover_speed_screen(None, screen, settings, game_clocks, actors),
        'gameover_points': lambda : GameOverScreens.draw_gameover_points_screen(None, screen, settings, game_clocks, actors),
        'question_time': lambda : QuestionScreens.draw_question_screen(None, screen, game_questions)
    }
    if current_screen in screen_actions:
        screen_actions[current_screen]()




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
        shuffle(game_questions.questions_e)
        shuffle(game_questions.questions_m)
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
        actors.backgrounds.clear()
        actors.scroll = 0
        current_screen = 'start'
    elif clicked_actor == 'easy' and (current_screen == 'difficulty_speed' or current_screen == 'difficulty_points'):
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
            if box.collidepoint(pos) and game_questions.question_screen == 'points_easy':
                current_screen, game_questions.answer = game_questions.update_game_state_points(index, game_questions.question_e, sounds, 'points_easy')
                game_questions.question_e = game_questions.questions_e.pop(0)
                game_questions.questions_e.append(game_questions.question_e)
            elif box.collidepoint(pos) and game_questions.question_screen == 'speed_easy':
                print(f"Box {index} clicked, updating game state")
                current_screen, game_questions.answer = game_questions.update_game_state_speed(index, game_questions.question_e, sounds, 'speedrun_easy')
                game_questions.question_e = game_questions.questions_e.pop(0)
                game_questions.questions_e.append(game_questions.question_e)
            elif box.collidepoint(pos) and game_questions.question_screen == 'speed_medium':
                current_screen, game_questions.answer = game_questions.update_game_state_speed(index, game_questions.question_m, sounds, 'speedrun_medium')
                game_questions.question_m = game_questions.questions_m.pop(0)
                game_questions.questions_m.append(game_questions.question_m)
            elif box.collidepoint(pos) and game_questions.question_screen == 'points_medium':
                current_screen, game_questions.answer = game_questions.update_game_state_speed(index, game_questions.question_m, sounds, 'points_medium')
                game_questions.question_m = game_questions.questions_m.pop(0)
                game_questions.questions_m.append(game_questions.question_m)


def update():
    global current_screen
    if current_screen == 'difficulty_speed' or current_screen == 'difficulty_points' or current_screen == 'start' or current_screen == 'gamemode':
        actors.static_update_animations()
        actors.scroll = 0
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
        current_screen = points_level_medium(game_clocks, actors, game_questions, current_screen, sounds)


pgzrun.go()