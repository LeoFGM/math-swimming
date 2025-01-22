from pgzero.rect import Rect
from random import randint, shuffle
from changevar import GameClocks



class GameQuestions:
    def __init__(self):
        self.main_box = Rect(0, 0, 420, 250)
        self.timer_box = Rect(0, 0, 230, 125)
        self.answer_box1 = Rect(0, 0, 300, 75)
        self.answer_box2 = Rect(0, 0, 300, 75)
        self.answer_box3 = Rect(0, 0, 300, 75)
        self.answer_box4 = Rect(0, 0, 300, 75)
        self.time_left_e = 10
        self.main_box.move_ip(50, 50)
        self.timer_box.move_ip(510, 50)
        self.answer_box1.move_ip(50, 375)
        self.answer_box2.move_ip(450, 375)
        self.answer_box3.move_ip(50, 475)
        self.answer_box4.move_ip(450, 475)
        self.answer_boxes = [self.answer_box1, self.answer_box2, self.answer_box3, self.answer_box4]
        self.question_screen = None
        self.q1_e = ["What is the value of x in: 2x + 3 = 9", "5", "1", "3", "8", 3]
        self.q2_e = ["How many sides does a decagon have?", "5", "10", "7", "4", 2]
        self.q3_e = ["What's the square root of 81?", "9", "3", "81", "18", 1]
        self.q4_e = ["What is the 20% of 2500?", "25", "75", "125", "500", 4]

        self.questions_e = [self.q1_e, self.q2_e, self.q3_e, self.q4_e]
        shuffle(self.questions_e)
        self.question_e = self.questions_e.pop(0)
        self.answer = None

    def update_game_state_points(self, i, sound):
        correct_answer_index = self.question_e[5]
        if i == correct_answer_index and self.question_screen == 'points':
            print("Correct answer")
            sound.correct_answer.play()
            return 'points_easy','correct'
        else:
            print("incorrect answer")
            sound.incorrect_answer.play()
            return 'points_easy','incorrect'

    def update_game_state_speed(self, i, sound):
        correct_answer_index = self.question_e[5]
        if i == correct_answer_index and self.question_screen == 'speed':
            print("Correct answer")
            sound.correct_answer.play()
            return 'speedrun_easy','correct'
        else:
            print("incorrect answer")
            sound.incorrect_answer.play()
            return 'speedrun_easy','incorrect'

    #Easy questions









#Medium questions






#Hard questions






#Extreme questions