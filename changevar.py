from pgzero import clock



class GameClocks:
    def __init__(self):
        self.count_max = 60
        self.count_down_max = 60
        self.count = 0
        self.show_count = False
        self.action = 0
        self.action1 = 0
        self.score = 0
        self.active_timer = 0
        self.time_duration = 5

    def countup(self):
        if self.count < self.count_max:
            self.count += 1
            clock.schedule(self.countup, 1)
        elif self.count >= self.count_max:
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

    def start_timer(self):
        self.active_timer = self.time_duration
        self.decrement_timer()

    def decrement_timer(self):
        if self.active_timer > 0:
            self.active_timer -= 0.16
            clock.schedule(self.decrement_timer, 0.17)
        else:
            self.stop_timer()

    def stop_timer(self):
        self.active_timer = 0














