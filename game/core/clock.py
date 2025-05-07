import time
from gc import callbacks

from pgzero import clock



class GameClocks:
    def __init__(self):
        #Gameplay attributes
        self.count_max = 90
        self.count_down_max = 90
        self.count = 0
        self.show_count = False
        self.action = 0
        self.score = 0
        #Timers attributes
        self.active_timers = {}
        self.level_start_time = 0
        self.level_elapsed_time = 0
        self.time_paused = 0
        self.is_paused = False
        self.last_update_time = time.time()

        self.shield = 0


    #Level's timer logic
    def start_level_timer(self):
        self.level_start_time = time.time()
        self.level_elapsed_time = 0
        self.is_paused = False

    def pause_level_timer(self):
        if not self.is_paused:
            self.time_paused = time.time()
            self.is_paused = True

    def resume_level_timer(self):
        if self.is_paused:
            pause_duration = time.time() - self.time_paused
            self.level_start_time += pause_duration
            self.is_paused = False

    def get_elapsed_time(self):
        if self.is_paused:
            return self.level_elapsed_time
        return time.time() - self.level_start_time

    def countup(self):
        if self.count_max == 90:
            self.start_level_timer()
        if self.count < self.count_max:
            self.count_max -= 1
            clock.schedule(self.countup, 1)
        elif self.count == self.count_max:
            self.level_elapsed_time = self.get_elapsed_time()
            return 'gameover_speed'

    def countdown(self):
        if self.count_down_max > 0:
            self.count_down_max -= 1
            clock.schedule(self.countdown, 1)
        elif self.count_down_max == 0:
            'gameover_points'

    def reset_variables(self):
        self.count = 0
        self.count_max = 90
        self.count_down_max = 90
        self.action = 0
        self.score = 0
        self.level_elapsed_time = 0
        self.level_start_time = 0
        self.shield = 0
        self.time_paused = 0
        self.is_paused = False
        return

    #General timer methods
    def start_timer(self, timer_name, duration, callback=None):
        self.active_timers[timer_name] = {
            'duration': duration,
            'remaining': duration,
            'start_time': time.time(),
            'callback': callback
        } #Dict to save all values necessary

    def update_timers(self, dt, callback=None):
        current_time = time.time()
        elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        for timer_name in list(self.active_timers.keys()): #Creates a copy of the dict
            if timer_name in self.active_timers:  #In case there's more than 1 timer at the same time
                timer = self.active_timers[timer_name]
                timer['remaining'] = max(0, timer['remaining'] - elapsed)

                if timer['remaining'] <= 0: #Action when the timer reaches 0
                    if timer['callback']:
                        timer['callback']()
                    if callback and timer_name == 'question_timer':
                        callback()
                    self.stop_timer(timer_name)


    def stop_timer(self, timer_name):
        if timer_name in self.active_timers:
            del self.active_timers[timer_name]

    def get_timer_remaining(self, timer_name):
        if timer_name in self.active_timers:
            return int(self.active_timers[timer_name]['remaining'])
        return 0















