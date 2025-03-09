from random import shuffle
from pgzero.rect import Rect
from game.questions.question_data import EASY_QUESTIONS, MEDIUM_QUESTIONS


class GameQuestions:
    def __init__(self):
        self.main_box = Rect(0, 0, 420, 250)
        self.timer_box = Rect(0, 0, 230, 125)
        self.answer_boxes = [Rect(0, 0 , 300, 75) for _ in range(4)]
        self.time_left_e = 10
        self._position_boxes()

        self.question_screen = None
        self.used_questions = []
        self.questions_e = EASY_QUESTIONS.copy()
        self.questions_m = MEDIUM_QUESTIONS.copy()

        self.question_e = None
        self.question_m = None
        self.answer = None

    def _position_boxes(self):
        self.main_box.move_ip(50, 50)
        self.timer_box.move_ip(510, 50)
        for i, box in enumerate(self.answer_boxes):
            x = 50 if i % 2 == 0 else 450
            y = 375 if i < 2 else 475
            box.move_ip(x, y)

    def get_first_question(self, current_screen):
        if 'easy' in current_screen:
            self.question_e = self._get_next_question(self.questions_e)
        elif 'medium' in current_screen:
            self.question_m = self._get_next_question(self.questions_m)

    def _get_next_question(self, questions):
        if not questions:
            questions = EASY_QUESTIONS.copy() if questions == self.questions_e else MEDIUM_QUESTIONS.copy()
            shuffle(questions)
        return questions.pop(0)

    def update_question_state(self, i, question, sound, current_screen):
        correct_answer_index = question["correct"]
        if i == correct_answer_index:
            print("Correct answer")
            sound.correct_answer.play()
            self.answer = 'correct'
        else:
            print("incorrect answer")
            sound.incorrect_answer.play()
            self.answer = 'incorrect'
        self.reset_questions()
        return current_screen, self.answer

    def draw_questions(self, screen, time_left, question):
        screen.draw.filled_rect(self.main_box, "sky blue")
        screen.draw.filled_rect(self.timer_box, "sky blue")
        for box in self.answer_boxes:
            screen.draw.filled_rect(box, "medium slate blue")
        screen.draw.textbox(str(time_left), self.timer_box, color="black")
        screen.draw.textbox(question["question"], self.main_box, color="black")
        for index, box in enumerate(self.answer_boxes):
            screen.draw.textbox(question["answers"][index], box, color="black")

    def analyze_answer(self, game_clocks):
        if self.answer == 'correct':
            if 'points' in self.question_screen:
                game_clocks.score += 10
            elif 'speed' in self.question_screen:
                game_clocks.count_max -= 5
        elif self.answer == 'incorrect':
            if 'points' in self.question_screen:
                game_clocks.score -= 10
            elif 'speed' in self.question_screen:
                game_clocks.count_max += 5

        self.answer = None
        self.question_screen = None


    def reset_questions(self):
        if 'easy' in self.question_screen:
            self.questions_e = EASY_QUESTIONS.copy()
            shuffle(self.questions_e)
        elif 'medium' in self.question_screen:
            self.questions_m = MEDIUM_QUESTIONS.copy()
            shuffle(self.questions_m)












