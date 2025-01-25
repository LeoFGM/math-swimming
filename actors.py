from pgzero.actor import Actor

from pgzero.keyboard import keyboard
from settings import settings
from random import randint

class GameActors:

#All objects images
    game_name_states = ["title", "title_2", "title_3", "title_4"]  # Main title images
    gamemode_states = ["selgamemode_1", "selgamemode_2", "selgamemode_3", "selgamemode_4"]  # Select gamemode images
    title_states_diff = ["selectdiff", "selectdiff_1", "selectdiff_2", "selectdiff_3", "selectdiff_4"]  # Select difficulty images
    title_states_easy = ["easy", "easy_1", "easy_2", "easy_3", "easy_4"]  # Easy animation images
    title_states_medium = ["medium", "medium_1", "medium_2", "medium_3", "medium_4"]  # Medium animation images
    title_states_hard = ["hard", "hard_1", "hard_2", "hard_3", "hard_4"]  # Hard animation images
    title_states_extreme = ["extreme", "extreme_1", "extreme_2", "extreme_3", "extreme_4"]  # Extreme animation images
    log_states = ["log", "log_1"]  # log animation images
    swimmer_states = ["swimmer", "swimmer_1", "swimmer_2", "swimmer_3"]  # swimmer not-hit animation images
    swimmer_states_hit = ["swimmer", "swimmer_hit", "swimmer_1", "swimmer_hit", "swimmer_2","swimmer_3"]  # swimmer hit animation images
    powerup_states = ["powerup", "powerup_1", "powerup_2"]  # powerup animation images
    coin_states = ["coin", "coin_1", "coin_2"]  # coin animation images
    shark_states = ["shark", "shark_1", "shark_2", "shark_3", "shark_4", "shark_5", "shark_6", "shark_7", "shark_8", "shark_9", "shark_10", "shark_11", "shark_12", "shark_13"]
    q_block_states = ["question_block", "question_block_1"]

#All animation variables
    number_of_updates = 0  # titles
    number_of_updates1 = 0
    number_of_updates_log = 0  # logs
    number_of_updates_swimmer = 0
    number_of_updates_powerup = 0
    number_of_updates_coin = 0
    number_of_updates_block = 0
    number_of_updates_shark = 0
    hit_updates = 0

#Background variables

    scroll = 0
    neg = 1
    backgrounds = []

#Object creation variables
    logs = []
    powerups = []
    coins = []
    x = 250
    def __init__(self):
        self.start = Actor("start", pos=(settings.CENTER_X, 550))
        self.speedrun = Actor("speedrun", pos=(settings.CENTER_X - 200, 450))
        self.pointsmania = Actor("pointsmania", pos=(settings.CENTER_X + 200, 450))
        self.gamename = Actor("title", pos=(settings.CENTER_X, 250))
        self.gamemode = Actor("selgamemode_1", pos=(settings.CENTER_X, 250))
        self.difficulty = Actor("selectdiff", pos=(settings.CENTER_X, 175))
        self.easy = Actor("easy", pos=(settings.CENTER_X - 200, 350))
        self.medium = Actor("medium", pos=(settings.CENTER_X + 200, 350))
        self.hard = Actor("hard", pos=(settings.CENTER_X - 200, 525))
        self.extreme = Actor("extreme", pos=(settings.CENTER_X + 200, 525))
        self.goback = Actor("goback", pos=(50, 580))
        self.q_block = Actor("question_block", pos=(settings.CENTER_X, randint(-2000, -1600)))
        self.shark = Actor("shark", pos=(randint(190, 625), randint(-800, -400)))
        self.swimmer = Actor("swimmer", pos=(settings.CENTER_X, 550))
        self.not_hit = True
        self.powerup_collision = False

    def new_log(self):
        global logs, x
        log_new = Actor("log")
        log_new.pos = self.x, randint(-800, -500)
        self.logs.append(log_new)
        self.x += 150

    def new_coin(self):
        global coins
        coin_new = Actor("coin")
        coin_new.pos = randint(175, 625), randint(-800, -300)
        self.coins.append(coin_new)

    def new_power_up(self):
        global powerups, logs
        powerup_new = Actor("powerup")
        powerup_new.pos = self.logs[randint(0, 2)].x, self.logs[randint(0, 2)].y + 125
        self.powerups.append(powerup_new)

    def create_actors(self, whole):
        for i in whole:
            i.draw()

    def stop_swimmer_hit_animation(self):
        self.not_hit = True

    def stop_powerup(self):
        self.powerup_collision = False

    def draw_start_screen(self):
        self.start.draw()
        self.gamename.draw()

    def draw_gamemode_screen(self):
        self.speedrun.draw()
        self.pointsmania.draw()
        self.gamemode.draw()
        self.goback.draw()

    def draw_difficulty_screen(self):
        self.difficulty.draw()
        self.easy.draw()
        self.medium.draw()
        self.hard.draw()
        self.extreme.draw()
        self.goback.draw()


    def actors_image_change(self, actor, states):
        current = states.pop(0)
        states.append(current)
        actor.image = current

    def actors_animation(self, updates, rate, actor, states):
        if updates == rate:
            self.actors_image_change(actor, states)
            updates = 0
        else:
            updates += 1

    def difficulties_animation(self):
        self.actors_image_change(self.difficulty, self.title_states_diff)
        self.actors_image_change(self.easy, self.title_states_easy)
        self.actors_image_change(self.medium, self.title_states_medium)
        self.actors_image_change(self.hard, self.title_states_hard)
        self.actors_image_change(self.extreme, self.title_states_extreme)

    def handle_mouse_down(self, pos):
        if self.start.collidepoint(pos):
            return 'start'
        elif self.speedrun.collidepoint(pos):
            return 'speedrun'
        elif self.pointsmania.collidepoint(pos):
            return 'pointsmania'
        elif self.easy.collidepoint(pos):
            return 'easy'
        elif self.medium.collidepoint(pos):
            return 'medium'
        elif self.hard.collidepoint(pos):
            return 'hard'
        elif self.extreme.collidepoint(pos):
            return 'extreme'
        elif self.goback.collidepoint(pos):
            return 'goback'
        return None

    def set_background(self,screen):
        global neg
        screen.clear()
        for i in range(0, 3):
            bg = screen.blit("river", (0, i * (600 * self.neg) + self.scroll))
            self.backgrounds.append(bg)
            self.neg = -1

    def moving_bg(self):
        global scroll
        for back in self.backgrounds:
            self.scroll += 0.0003
        if abs(self.scroll) > 600:
            self.scroll = 0

    def moving(self, actor, objects, quantity, quantity2):
        if keyboard.left and (actor.x > 190):
            actor.x -= quantity
        if keyboard.right and (actor.x < 625):
            actor.x += quantity
        if keyboard.left and (actor.x > 190) and objects:
            actor.x -= quantity2
        if keyboard.right and (actor.x < 625) and objects:
            actor.x += quantity2



#All animation images



