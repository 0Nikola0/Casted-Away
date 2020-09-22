import pygame
import pymunk as pm
import src.settings as s


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, top_left=True):
        super(Wall, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(s.BLACK)
        self.rect = self.image.get_rect()

        if top_left is True:
            self.rect.topleft = pos
        else:
            self.rect.bottomright = pos
