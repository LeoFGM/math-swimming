from game.constants import QuestionStates, GameState
from game.core.context import GameContext


class QuestionScreens:

    def draw_question_screen(self, screen, context: GameContext()):

        global time_left

        question_data = {
            'speed_easy': context.questions.question_e,
            'points_easy': context.questions.question_e,
            'speed_medium': context.questions.question_m,
            'points_medium': context.questions.question_m
        }


        if context.questions.question_screen in question_data:
            question = question_data[context.questions.question_screen]
            if 'question_timer' in context.clock.active_timers:
                time_left = context.clock.active_timers['question_timer']['remaining']
            context.questions.draw_questions(screen, time_left=str(int(time_left)), question=question)
        else:
            print(f"Error: Invalid question screen type: {context.questions.question_screen}")

    def handle_question_screen(self, context: GameContext(), pos, sounds):


        for index, box in enumerate(context.questions.answer_boxes, start=0):
            if box.collidepoint(pos):
                question_screen_map = {
                    QuestionStates.POINTS_EASY: lambda: context.questions.update_question_state(index,
                                                                                                context.questions.question_e,
                                                                                                sounds,
                                                                                                GameState.POINTS_EASY),
                    QuestionStates.SPEED_EASY: lambda: context.questions.update_question_state(index,
                                                                                               context.questions.question_e,
                                                                                               sounds,
                                                                                               GameState.SPEEDRUN_EASY),
                    QuestionStates.POINTS_MEDIUM: lambda: context.questions.update_question_state(index,
                                                                                                  context.questions.question_m,
                                                                                                  sounds,
                                                                                                  GameState.POINTS_MEDIUM),
                    QuestionStates.SPEED_MEDIUM: lambda: context.questions.update_question_state(index,
                                                                                                 context.questions.question_m,
                                                                                                 sounds,
                                                                                                 GameState.SPEEDRUN_MEDIUM)
                }
                if context.questions.question_screen in question_screen_map:
                    context.current_screen, context.questions.answer = question_screen_map[
                        context.questions.question_screen]()
                    context.questions.analyze_answer(context.clock)
                    context.questions.get_first_question(context.current_screen)
            else:
                print(f"Answer box {index} not clicked")

