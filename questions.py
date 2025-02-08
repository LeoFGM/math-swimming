from random import shuffle
from pgzero.rect import Rect


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
        self.used_questions = []
        #Easy questions
        self.q1_e = ["What is the value of x in: 2x + 3 = 9", "5", "1", "3", "8", 3]
        self.q2_e = ["How many sides does a decagon have?", "5", "10", "7", "4", 2]
        self.q3_e = ["What's the square root of 81?", "9", "3", "81", "18", 1]
        self.q4_e = ["What is the 20% of 2500?", "25", "75", "125", "500", 4]
        self.q5_e = ["What is the value of 13^2?", "121", "100", "196", "169", 4]
        self.q6_e = ["What is the perimeter of a square with a 5cm side?", "10", "20", "25", "15", 2]
        self.q7_e = ["If x = 3, y = 2, what's the value of 2x + 3y?", "8", "14", "12", "11", 3]
        self.q8_e = ["What is the square root of 8100?", "81", "30", "60", "90", 4]
        self.q9_e = ["What's the next number of the sequence. 2, 4, 8, 16,___", "26", "24", "32", "36", 3]
        self.q10_e = ["What's the value of 4!?", "12", "24", "120", "6", 2]

        self.questions_e = [self.q1_e, self.q2_e, self.q3_e, self.q4_e, self.q5_e, self.q6_e, self.q7_e, self.q8_e, self.q9_e, self.q10_e]
        shuffle(self.questions_e)
        self.question_e = self.questions_e.pop(0)
        #Medium questions
        self.q1_m = ["What is the value of x in the equation 2x + 5 = 15?", "4", "6", "5", "3", 3]
        self.q2_m = ["What is 15×12?", "180", "200", "150", "165", 1]
        self.q3_m = ["What is the square root of 256?", "14", "16", "18", "20", 2]
        self.q4_m = ["What is the area of a triangle with a base of 10 and a height of 8?", "50", "40", "80", "30", 2]
        self.q5_m = ["If a car travels 120 km in 2 hours, what is its average speed?", "50 km/h", "70 km/h", "60 km/h", "80 km/h", 3]

        self.questions_m = [self.q1_m, self.q2_m, self.q3_m, self.q4_m, self.q4_m, self.q5_m]
        self.question_m = self.questions_m.pop(0)

        self.answer = None



    def update_question_state(self, i, question, sound, current_screen):
        correct_answer_index = question[5]
        if i == correct_answer_index:
            print("Correct answer")
            sound.correct_answer.play()
            return current_screen,'correct'
        else:
            print("incorrect answer")
            sound.incorrect_answer.play()
            return current_screen,'incorrect'

    def draw_questions(self, screen, time_left, question):
        screen.draw.filled_rect(self.main_box, "sky blue")
        screen.draw.filled_rect(self.timer_box, "sky blue")
        for box in self.answer_boxes:
            screen.draw.filled_rect(box, "medium slate blue")
        screen.draw.textbox(str(time_left), self.timer_box, color="black")
        screen.draw.textbox(question[0], self.main_box, color="black")
        for index, box in enumerate(self.answer_boxes, start=1):
            screen.draw.textbox(question[index], box, color="black")

    def reset_questions_easy(self):
        self.questions_e = [self.q1_e, self.q2_e, self.q3_e, self.q4_e, self.q5_e, self.q6_e, self.q7_e, self.q8_e, self.q9_e, self.q10_e
        ]
        shuffle(self.questions_e)
        self.question_e = self.questions_e.pop(0)

    def reset_questions_medium(self):
        self.questions_m = [self.q1_m, self.q2_m, self.q3_m, self.q4_m, self.q4_m, self.q5_m]
        shuffle(self.questions_m)
        self.question_m = self.questions_m.pop(0)

        #Easy questions









#Medium questions






#Hard questions






#Extreme questions