from random import randint
from pgzero.actor import Actor
from pgzero.clock import clock
from pgzero.keyboard import keyboard
from actors import *
from changevar import *
from screen import *

#New actors



#Indexing function

def index_lists(whole):
    for index, each  in enumerate(whole):
        index += 1

#Drawing functions




#Mobility functions

def moving(screen, objects):
    if keyboard.left and (swimmer.x > 190) and screen:
        swimmer.x -= 3
    if keyboard.right and (swimmer.x < 625) and screen:
        swimmer.x += 3
    if keyboard.left and (swimmer.x > 190) and objects:
        swimmer.x -= 5
    if keyboard.right and (swimmer.x < 625) and objects:
        swimmer.x += 5

#Changing screens

def screen_change():
    return False, True





