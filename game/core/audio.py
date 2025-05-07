import threading
import time

import pygame

class MusicalActions:
    MUSIC_FOLDER = "music"
    MUSIC_EXTENSION = ".ogg"
    def __init__(self):
        self.music_list = {'speedrun_easy': "strength", 'points_easy': "behemoth", 'speedrun_medium': "monster",'points_medium': "hero"}

        self.current_music = None
        self.current_position = 0
        self.restore_allowed = True


    def change_music_temporarily(self, new_music, duration, initial_music):
        if pygame.mixer.music.get_busy(): #Gets the last position of the music
            current_music = initial_music
            current_position = pygame.mixer.music.get_pos()
            pygame.mixer.music.pause()

        #Pause current music
        pygame.mixer.music.pause()

        #Play new music
        pygame.mixer.music.load(f"{self.MUSIC_FOLDER}/{new_music}{self.MUSIC_EXTENSION}")
        pygame.mixer.music.play()
        pygame.mixer.music.fadeout(duration * 1000)

        #Unpause initial music
        def restore_music():
            print(f"Restoring {initial_music}")
            try:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                if self.restore_allowed and current_music:
                    pygame.mixer.music.load(f"{self.MUSIC_FOLDER}/{current_music}{self.MUSIC_EXTENSION}")
                    pygame.mixer.music.play(start=current_position / 1000)
            except pygame.error as e:
                print(f"Error al intentar restaurar la música: {e}")

        def delayed_restore():
            time.sleep(duration)
            if self.restore_allowed:
                restore_music()
        threading.Thread(target=delayed_restore).start()

    def disable_music_restore(self):
        #Disables music restoration to avoid problems
        self.restore_allowed = False
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(1000)
        except pygame.error as e:
            print(f"Error al detener la música: {e}")

    def enable_music_restore(self):
        #Enables it again
        self.restore_allowed = True




