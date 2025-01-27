import threading
import pygame
import time

current_music = None
current_position = 0

MUSIC_FOLDER = "music"
MUSIC_EXTENSION = ".ogg"

def change_music_temporarily(new_music, duration, initial_music):
    global current_music, current_position
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
        pygame.mixer.music.stop()
        if current_music:
            pygame.mixer.music.load(f"{MUSIC_FOLDER}/{current_music}{MUSIC_EXTENSION}")
            pygame.mixer.music.play(start=current_position / 1000)

    def delayed_restore():
        time.sleep(duration)
        restore_music()

    threading.Thread(target=delayed_restore).start()