from actors import *


#To make animations more fluid





#Object in-game animations




def pu_swimmer():
    global number_of_updates_swimmer
    if number_of_updates_swimmer == 7:
        actors_animation(swimmer, swimmer_states)
        number_of_updates_swimmer = 0
    else:
        number_of_updates_swimmer += 1

def log_animation(log):
    global number_of_updates_log
    if number_of_updates_log == 10:
        actors_animation(log, log_states)
        number_of_updates_log = 0
    else:
        number_of_updates_log += 1

def not_hit_swimmer():
    global number_of_updates_swimmer
    if number_of_updates_swimmer == 10:
        actors_animation(swimmer, swimmer_states)
        number_of_updates_swimmer = 0
    else:
        number_of_updates_swimmer += 1

def powerups_animation(powerup):
    global number_of_updates_powerup
    if number_of_updates_powerup == 10:
        actors_animation(powerup, powerup_states)
        number_of_updates_powerup = 0
    else:
        number_of_updates_powerup += 1

def coin_animation(coin):
    global number_of_updates_coin
    if number_of_updates_coin == 10:
        actors_animation(coin, coin_states)
        number_of_updates_coin = 0
    else:
        number_of_updates_coin += 1
