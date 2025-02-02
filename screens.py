
class MenuScreens:
    def draw_start_screen(self, actors):
        actors.draw_actors(actors.start, actors.gamename)

    def draw_gamemode_screen(self, actors):
        actors.draw_actors(actors.speedrun, actors.pointsmania, actors.gamemode, actors.goback)

    def draw_difficulty_screen(self, actors):
        actors.draw_actors(actors.difficulty, actors.easy, actors.medium, actors.hard, actors.extreme, actors.goback)

class GameScreens:
    def draw_speedrun_easy_screen(self, screen, game_clocks, actors):
        actors.set_background(screen)
        actors.draw_actors(actors.swimmer, actors.q_block)
        actors.create_and_draw_actors(actors.logs, actors.powerups)
        screen.draw.text(f"Time: {game_clocks.count}", color="orange red", topleft=(20, 20), fontsize=40)

    def draw_points_easy_screen(self, screen, game_clocks, actors):
        actors.set_background(screen)
        actors.draw_actors(actors.swimmer, actors.q_block)
        actors.create_and_draw_actors(actors.logs, actors.coins)
        screen.draw.text(f"Time: {game_clocks.count_down_max}", color="orange red", topleft=(20, 20), fontsize=40)
        screen.draw.text(f"Score: {game_clocks.score}", color="orange red", topleft=(670, 20), fontsize=40)

    def draw_speedrun_medium_screen(self, screen, game_clocks, actors):
        actors.set_background(screen)
        actors.draw_actors(actors.swimmer, actors.q_block, actors.shark)
        actors.create_and_draw_actors(actors.logs, actors.powerups)
        screen.draw.text(f"Time: {game_clocks.count}", color="orange red", topleft=(20, 20), fontsize=40)

    def draw_points_medium_screen(self, screen, game_clocks, actors):
        actors.set_background(screen)
        actors.draw_actors(actors.swimmer, actors.q_block)
        actors.create_and_draw_actors(actors.logs, actors.coins)
        screen.draw.text(f"Time: {game_clocks.count_down_max}", color="orange red", topleft=(20, 20), fontsize=40)
        screen.draw.text(f"Score: {game_clocks.score}", color="orange red", topleft=(670, 20), fontsize=40)

class QuestionScreens:
    def draw_question_screen(self, screen, game_questions):
        print(f"Question: {game_questions.questions_e[0]}")
        print(f"Type of question: {type(game_questions.questions_e[0])}")

        question_data = {
            'speed_easy': game_questions.question_e,
            'points_easy': game_questions.question_e,
            'speed_medium': game_questions.question_m,
            'points_medium': game_questions.question_m
        }

        if game_questions.question_screen in question_data:
            game_questions.draw_questions(screen, time_left=10, question=question_data[game_questions.question_screen])

class GameOverScreens:
    def draw_gameover_speed_screen(self, screen, settings, game_clocks, actors):
        screen.draw.text(f"You completed the level in: {game_clocks.count} seconds!", color="black", center=settings.CENTER, fontsize=60)
        actors.goback.draw()

    def draw_gameover_points_screen(self, screen, settings, game_clocks, actors):
        screen.draw.text(f"You ended with: {game_clocks.score} points!", color="black", center=settings.CENTER, fontsize=60)
        actors.goback.draw()