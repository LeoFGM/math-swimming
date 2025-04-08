import time

from pgzero import clock



class GameClocks:
    def __init__(self):
        self.count_max = 60
        self.count_down_max = 60
        self.count = 0
        self.show_count = False
        self.action = 0
        self.score = 0
        self.active_timers = {}
        self.level_start_time = 0
        self.level_elapsed_time = 0
        self.time_paused = 0
        self.is_paused = False
        self.last_update_time = time.time()


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
        if self.count_max == 60:
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
        self.count_max = 60
        self.count_down_max = 60
        self.action = 0
        self.score = 0
        self.level_elapsed_time = 0
        self.level_start_time = 0
        self.time_paused = 0
        self.is_paused = False
        return

    def start_timer(self, timer_name, duration):
        self.active_timers[timer_name] = {
            'duration': duration,
            'remaining': duration,
            'start_time': time.time()
        }


    def update_timers(self, dt):
        current_time = time.time()
        elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        timer_names = list(self.active_timers.keys())

        for timer_name in timer_names:
            if timer_name in self.active_timers:  # Check if still exists
                timer = self.active_timers[timer_name]
                timer['remaining'] = max(0, timer['remaining'] - elapsed)

                if timer['remaining'] <= 0:
                    self.stop_timer(timer_name)

    def stop_timer(self, timer_name):
        if timer_name in self.active_timers:
            del self.active_timers[timer_name]

    def get_timer_remaining(self, timer_name):
        if timer_name in self.active_timers:
            return int(self.active_timers[timer_name]['remaining'])
        return 0















