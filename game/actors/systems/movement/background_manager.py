class BackgroundManager:
    SCROLL_INCREMENT = 1
    MAX_SCROLL = 600

    def __init__(self):
        self.scroll = 0
        self.neg = 1
        self.backgrounds = []
        self.is_inverted = False

    def set_background(self, screen):
        screen.clear()
        bg_image = "river_inverted" if self.is_inverted else "river"
        self.backgrounds = []
        for i in range(3):
            y_pos = i * (600 * self.neg) + self.scroll
            bg = screen.blit(bg_image, (0, y_pos))
            self.backgrounds.append(bg)
            self.neg = -1

    def toggle_inversion(self):
        self.is_inverted = not self.is_inverted

    def moving_bg(self):
        self.scroll += self.SCROLL_INCREMENT
        if abs(self.scroll) > self.MAX_SCROLL:
            self.scroll = 0