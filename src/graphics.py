"""
usage:
    sheet = spritesheet.SpriteSheet()
    image = sheet.get_image('player_idle', scale=(x,y))
"""

import pygame

file_name = "./assets/imgs/actors/1 Old_man/Old_man_attack.png"
old_man_size = (om_xs, om_ys) = (48, 48)

# NAME = {
#     '0': (om_xs * 1, om_ys * 0, *old_man_size),
#     '1': (om_xs * 2, om_ys * 0, *old_man_size),
#     '2': (),
#     '3': (),
# }

NAME = {str(i): (om_xs * i + 1, 0, *old_man_size) for i in range(4)}


class SpriteSheet:
    def __init__(self):
        self.source_image = pygame.image.load(file_name).convert_alpha()

    def get_image(self, name, scale=False):
        image = self.get_image_by_coordinates(*NAME[name])
        if scale:
            image = pygame.transform.scale(image, scale)

        return image

    def get_image_by_coordinates(self, x, y, width, height):
        image = pygame.Surface([width, height], pygame.SRCALPHA)
        image.blit(self.source_image, (0, 0), (x, y, width, height))

        return image
