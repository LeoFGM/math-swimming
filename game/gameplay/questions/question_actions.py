from random import shuffle
from pgzero.rect import Rect
from .question_data import EASY_QUESTIONS, MEDIUM_QUESTIONS
from game.constants import QuestionStates, Answers, GameState

from ...core.context import GameContext


class GameQuestions:
    def __init__(self):
        self.main_box = Rect(0, 0, 420, 250)
        self.timer_box = Rect(0, 0, 230, 125)
        self.answer_boxes = [Rect(0, 0 , 300, 75) for _ in range(4)]
        self.question_timer = None
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
            print(f"Answer box {i} positioned at: {box.topleft}")  # Debugging


    def get_first_question(self, current_screen):
        if GameState.SPEEDRUN_EASY == current_screen or GameState.POINTS_EASY == current_screen:
            self.question_e = self._get_next_question(self.questions_e)
        elif GameState.SPEEDRUN_MEDIUM == current_screen or GameState.POINTS_MEDIUM == current_screen:
            self.question_m = self._get_next_question(self.questions_m)

    def _get_next_question(self, questions):
        if not questions:
            questions = EASY_QUESTIONS.copy() if questions == self.questions_e else MEDIUM_QUESTIONS.copy()
            shuffle(questions)
        return questions.pop(0)

    def update_question_state(self, i, question, sound, target_screen):
        correct_answer_index = question["correct"]
        if i == correct_answer_index:
            print("Correct answer")
            sound.correct_answer.play()
            self.answer = Answers.CORRECT
        else:
            print("incorrect answer")
            sound.incorrect_answer.play()
            self.answer = Answers.INCORRECT
        self.reset_questions()
        return target_screen, self.answer

    def draw_questions(self, screen, time_left, question):
        screen.draw.filled_rect(self.main_box, "sky blue")
        screen.draw.filled_rect(self.timer_box, "sky blue")
        for box in self.answer_boxes:
            screen.draw.filled_rect(box, "medium slate blue")

        screen.draw.filled_rect(self.timer_box, "sky blue")
        screen.draw.textbox(str(int(time_left)), self.timer_box, color="black")

        screen.draw.textbox(question["question"], self.main_box, color="black")
        for index, box in enumerate(self.answer_boxes):
            screen.draw.textbox(question["answers"][index], box, color="black")

    def analyze_answer(self, game_clocks):
        if self.answer == Answers.CORRECT:
            if 'points' in self.question_screen:
                game_clocks.score += 10
            elif 'speed' in self.question_screen:
                game_clocks.count_max -= 5
        elif self.answer == Answers.INCORRECT:
            if 'points' in self.question_screen:
                game_clocks.score -= 10
            elif 'speed' in self.question_screen:
                game_clocks.count_max += 5

        self.answer = None
        self.question_screen = None


    def reset_questions(self):
        if QuestionStates.SPEED_EASY == self.question_screen or QuestionStates.POINTS_EASY == self.question_screen:
            self.questions_e = EASY_QUESTIONS.copy()
            shuffle(self.questions_e)
        if QuestionStates.SPEED_MEDIUM == self.question_screen or QuestionStates.POINTS_MEDIUM == self.question_screen:
            self.questions_m = MEDIUM_QUESTIONS.copy()
            shuffle(self.questions_m)

    def on_timeout(self, context: GameContext(), sounds):
        # Determine which game mode to return to
        if self.question_screen == QuestionStates.POINTS_EASY:
            target_screen = GameState.POINTS_EASY
        elif self.question_screen == QuestionStates.POINTS_MEDIUM:
            target_screen = GameState.POINTS_MEDIUM
        elif self.question_screen == QuestionStates.SPEED_EASY:
            target_screen = GameState.SPEEDRUN_EASY
        elif self.question_screen == QuestionStates.SPEED_MEDIUM:
            target_screen = GameState.SPEEDRUN_MEDIUM
        else:
            target_screen = context.current_screen  # fallback

        # Process as wrong answer
        question = self.question_e if self.question_screen in [QuestionStates.POINTS_EASY, QuestionStates.SPEED_EASY] else self.question_m

        if question:
            # Mark answer as wrong
            context.current_screen, self.answer = self.update_question_state(
                -1, question, sounds, target_screen
            )
            self.analyze_answer(context.clock)
            self.get_first_question(target_screen)

            # Clear question screen state
            self.question_screen = None

            # Return to gameplay
            return target_screen

        return context.current_screen









