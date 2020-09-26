import pygame
import os
import src.settings as s
from src.scenes.main_menu import Background


IMGS_PATH = os.path.join("assets", "imgs", "menu", "")


class GameOver(Background):
    def __init__(self):
        super(Background, self).__init__()
        self.brightness = 255
        # TEXT
        self.image = pygame.image.load(IMGS_PATH + "game_over.png")
        self.rect = self.image.get_rect()
        self.rect.center = round(s.SCREEN_WIDTH / 2), 300

    def draw(self, surface):
        super(Background, self).draw(surface)
        self.update_brightness()

    def update_brightness(self):
        self.brightness = (self.brightness - 5) if self.brightness - 5 > 0 else 0
        self.image.fill((255, 255, 255, self.brightness), special_flags=pygame.BLEND_RGBA_MULT)
