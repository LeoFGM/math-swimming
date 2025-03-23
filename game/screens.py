class Screen:
    def __init__(self, game_actors):
        self.game_actors = game_actors

    def draw(self, screen, game_clocks, actor_movement):
        raise NotImplementedError("Subclasses must implement this method")

    def update_static_screen(self, actor_animation, actor_movement, current_screen):
        actor_animation.static_update_animations()
        actor_movement.scroll = 0
        return current_screen

    def update_game_screen(self, game_state, actor_movement, level_function, *args):
        actor_movement.moving_bg()
        return level_function(*args)

class MenuScreens(Screen):
    def draw_start_screen(self, screen):
        self.game_actors.draw_actors(self.game_actors.start, self.game_actors.gamename)

    def draw_gamemode_screen(self, screen):
        self.game_actors.draw_actors(self.game_actors.speedrun, self.game_actors.pointsmania, self.game_actors.gamemode, self.game_actors.goback)

    def draw_difficulty_screen(self, screen):
        self.game_actors.draw_actors(self.game_actors.difficulty, self.game_actors.easy, self.game_actors.medium, self.game_actors.hard, self.game_actors.extreme, self.game_actors.goback)

class GameScreens(Screen):
    def draw_speedrun_easy_screen(self, screen, game_clocks, game_actors, actor_movement):
        actor_movement.set_background(screen)
        game_actors.draw_actors(game_actors.swimmer, game_actors.q_block, game_actors.glasses)
        game_actors.create_and_draw_actors(game_actors.logs, game_actors.powerups)
        screen.draw.text(f"Time: {game_clocks.count}", color="orange red", topleft=(20, 20), fontsize=40)
        if game_actors.powerup_collision:
            screen.draw.text(f"Powerup activated for: {int(game_clocks.active_timer)}s", topleft=(20,60), fontsize=30, color="orange red")

    def draw_points_easy_screen(self, screen, game_clocks, game_actors, actor_movement):
        actor_movement.set_background(screen)
        game_actors.draw_actors(game_actors.swimmer, game_actors.q_block, game_actors.glasses)
        game_actors.create_and_draw_actors(game_actors.logs, game_actors.coins)
        screen.draw.text(f"Time: {game_clocks.count_down_max}", color="orange red", topleft=(20, 20), fontsize=40)
        screen.draw.text(f"Score: {game_clocks.score}", color="orange red", topleft=(660, 20), fontsize=40)

    def draw_speedrun_medium_screen(self, screen, game_clocks, game_actors, actor_movement):
        actor_movement.set_background(screen)
        game_actors.draw_actors(game_actors.swimmer, game_actors.q_block, game_actors.shark)
        game_actors.create_and_draw_actors(game_actors.logs, game_actors.powerups)
        screen.draw.text(f"Time: {game_clocks.count}", color="orange red", topleft=(20, 20), fontsize=40)
        if game_actors.powerup_collision:
            screen.draw.text(f"Powerup activated for: {int(game_clocks.active_timer)}s", topleft=(20,60), fontsize=30, color="orange red")

    def draw_points_medium_screen(self, screen, game_clocks, game_actors, actor_movement, comp_actors):
        actor_movement.set_background(screen)
        game_actors.draw_actors(game_actors.swimmer, game_actors.q_block, game_actors.bear)
        game_actors.create_and_draw_actors(game_actors.logs, game_actors.coins, game_actors.powerups)
        screen.draw.text(f"Time: {game_clocks.count_down_max}", color="orange red", topleft=(20, 20), fontsize=40)
        screen.draw.text(f"Score: {game_clocks.score}", color="orange red", topleft=(660, 20), fontsize=40)
        comp_actors.pooping()
        if game_actors.powerup_collision:
            screen.draw.text(f"Powerup activated for: {int(game_clocks.active_timer)}s", topleft=(20,60), fontsize=30, color="orange red")
        if "pooping_time" in comp_actors.poop_pos:
            game_actors.poop.draw()

class QuestionScreens:

    def draw_question_screen(self, screen, game_questions):

        question_data = {
            'speed_easy': game_questions.question_e,
            'points_easy': game_questions.question_e,
            'speed_medium': game_questions.question_m,
            'points_medium': game_questions.question_m
        }


        if game_questions.question_screen in question_data:
            question = question_data[game_questions.question_screen]
            game_questions.draw_questions(screen, time_left=10, question=question)
        else:
            print(f"Error: Invalid question screen type: {game_questions.question_screen}")

class GameOverScreens(Screen):
    def draw_gameover_speed_screen(self, screen, settings, game_clocks, game_actors):
        screen.draw.text(f"You completed the level in: {game_clocks.count} seconds!", color="black", center=settings.CENTER, fontsize=60)
        game_actors.goback.draw()

    def draw_gameover_points_screen(self, screen, settings, game_clocks, game_actors):
        screen.draw.text(f"You ended with: {game_clocks.score} points!", color="black", center=settings.CENTER, fontsize=60)
        game_actors.goback.draw()