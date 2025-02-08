import threading
import time

import pygame

current_music = None
current_position = 0

MUSIC_FOLDER = "music"
MUSIC_EXTENSION = ".ogg"

restore_allowed = True

def change_music_temporarily(new_music, duration, initial_music):
    global current_music, current_position, restore_allowed
    print("function activated")
    if pygame.mixer.music.get_busy():
        current_music = initial_music
        current_position = pygame.mixer.music.get_pos()
        pygame.mixer.music.pause()

    #Pause current music
    pygame.mixer.music.pause()

    #Play new music
    print(f"Playing temporary music: {new_music}")
    pygame.mixer.music.load(f"{MUSIC_FOLDER}/{new_music}{MUSIC_EXTENSION}")
    pygame.mixer.music.play()
    pygame.mixer.music.fadeout(duration * 1000)

    #Unpause initial music
    def restore_music():
        global  current_music, current_position
        print(f"Restoring {initial_music}")
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            if restore_allowed and current_music:
                pygame.mixer.music.load(f"{MUSIC_FOLDER}/{current_music}{MUSIC_EXTENSION}")
                pygame.mixer.music.play(start=current_position / 1000)
        except pygame.error as e:
            print(f"Error al intentar restaurar la música: {e}")

    def delayed_restore():
        time.sleep(duration)
        if restore_allowed:
            restore_music()
    threading.Thread(target=delayed_restore).start()

def disable_music_restore():
    global restore_allowed
    restore_allowed = False
    try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(1000)
    except pygame.error as e:
        print(f"Error al detener la música: {e}")

def enable_music_restore():
    global restore_allowed
    restore_allowed = True

music_list = {
    'speedrun_easy': "strength", 'points_easy': "behemoth", 'speedrun_medium': "monster", 'points_medium': "hero"
}

