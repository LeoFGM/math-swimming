#GLOBALS

class Settings:
    def __init__(self):
        #Screen settings
        self.WIDTH = 800
        self.HEIGHT = 600

        self.CENTER_X = self.WIDTH / 2
        self.CENTER_Y = self.HEIGHT / 2
        self.CENTER = (self.CENTER_X, self.CENTER_Y)

#Global setting instance
settings = Settings()