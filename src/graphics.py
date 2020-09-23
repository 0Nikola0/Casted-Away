"""
usage:
    sheet = spritesheet.SpriteSheet()
    image = sheet.get_image('player_idle', scale=(x,y))
"""

import pygame
import src.settings as s

size = sx, sy = s.SPRITES_SHEET_SPRITE_SIZE
# in ideal range(image_width) but I don't want to install labraries for that
NAME = {i: (sx * i + 1, 0, *size) for i in range(99)}


class SpriteSheet:
    def __init__(self, sheet_path):
        self.source_image = pygame.image.load(sheet_path).convert()
        self.source_image.set_colorkey(s.WHITE)
        # x = pygame.transform.threshold(self.source_image, self.source_image, s.WHITE) # For testing

    def get_image(self, name, scale=False):
        image = self.get_image_by_coordinates(*NAME[name])
        if scale:
            image = pygame.transform.scale(image, scale)

        return image

    def get_image_by_coordinates(self, x, y, width, height):
        image = pygame.Surface([width, height], pygame.SRCALPHA)
        image.blit(self.source_image, (0, 0), (x, y, width, height))

        return image
