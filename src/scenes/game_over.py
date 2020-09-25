import pygame
import os
import src.settings as s
from src.scenes.main_menu import Background


IMGS_PATH = os.path.join("assets", "imgs", "menu", "")


class Backgrund(Background):
    def __init__(self):
        super(Backgrund, self).__init__()
        self.brightness = 255
        # TEXT
        self.logo = pygame.image.load(IMGS_PATH + "game_over.png")
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = round(s.SCREEN_WIDTH / 2), 300

    def draw(self, surface):
        super(Backgrund, self).draw(surface)
        self.update_brightness()

    def update_brightness(self):
        self.brightness = (self.brightness - 5) if self.brightness - 5 > 0 else 0
        self.image.fill((255, 255, 255, self.brightness), special_flags=pygame.BLEND_RGBA_MULT)
