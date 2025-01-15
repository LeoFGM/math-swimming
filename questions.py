from pgzero.rect import Rect
from random import randint

main_box = Rect(0, 0, 420, 250)
timer_box = Rect(0, 0, 230, 125)
answer_box1 = Rect(0, 0, 300, 75)
answer_box2 = Rect(0, 0, 300, 75)
answer_box3 = Rect(0, 0, 300, 75)
answer_box4 = Rect(0, 0, 300, 75)
time_left_e = 10

main_box.move_ip(50, 50)
timer_box.move_ip(510, 50)
answer_box1.move_ip(50, 375)
answer_box2.move_ip(450, 375)
answer_box3.move_ip(50, 475)
answer_box4.move_ip(450, 475)

answer_boxes = [answer_box1, answer_box2, answer_box3, answer_box4]

def update_game_state_points(index, question, point_question_e, sound):
    if index == question[5] and point_question_e:
        sound.correct_answer.play()
        return True, False, False
    else:
        sound.incorrect_answer.play()
        return True, False, False

def update_game_state_speed(index, question, speed_question_e, sound):
    if index == question[5] and speed_question_e:
        sound.correct_answer.play()
        return  True, False, False
    else:
        sound.incorrect_answer.play()
        return True, False, False

#Easy questions
q1_e = ["What is the value of x in: 2x + 3 = 9", "5", "1", "3", "8", 3]
q2_e = ["How many sides does a decagon have?", "5", "10", "7", "4", 2]
q3_e = ["What's the square root of 81?", "9", "3", "81", "18", 1]
q4_e = ["What is the 20% of 2500?", "25", "75", "125", "500", 4]

questions_e = [q1_e, q2_e, q3_e, q4_e]
question_e = questions_e[randint(0,3)]








#Medium questions






#Hard questions






#Extreme questions