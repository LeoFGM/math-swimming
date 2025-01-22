from pgzero import clock


logs_already_created = False
powerups_already_created = False
coins_already_created = False
last_collision = 0
hit_animation = False
not_hit = True
powerup_collision = False





class GameClocks:

    def __init__(self):
        self.count_max = 60
        self.count_down_max = 60
        self.count = 0
        self.show_count = False
        self.action = 0
        self.action1 = 0
        self.score = 0

    def countup(self):
        if self.count < self.count_max:
            self.count += 1
            clock.schedule(self.countup, 1)
        elif self.count == self.count_max:
            return 'gameover_speed'

    def countdown(self):
        if self.count_down_max > 0:
            self.count_down_max -= 1
            clock.schedule(self.countdown, 1)
        elif self.count_down_max == 0:
            'gameover_points'

    def reset_variables(self):
        self.count = 0
        self.count_max = 60
        self.count_down_max = 60
        self.action = 0
        self.action1 = 0
        self.score = 0
        return












