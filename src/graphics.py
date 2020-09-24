import pygame
import src.settings as s

size = sx, sy = s.SPRITES_SHEET_SPRITE_SIZE
# in ideal range(image_width) but I don't want to install labraries for that
NAME = {i: (sx * i + 1, 0, *size) for i in range(99)}


class SpriteSheet:
    """Load sprite images from a sprite sheets

    usage:

    sheet = SpriteSheet(s.OLD_WOMAN_SPRITE_SHEETS["IDLE"])  # get only 1 sprite sheet (with IDLE image set)
    self.image = sh.get_image(0)  # get first image

    usage 2:

    sh = sh = {key: SpriteSheet(value) for key, value in s.OLD_WOMAN_SPRITE_SHEETS.items()}  # get all sprite sheets
    animation_length = 4  # number of images in 1 sheet

    self.animation_sets = []  # list of lists of all images / for select animation set
        for sh in shs:
            image_set = []  # list of all images in 1 sprite sheet
            for i in range(animation_length):
                image_set.append(shs[sh].get_image(i))
            self.animation_sets.append(image_set)

    self.state = {state_name: i for i, state_name in enumerate(shs)}

    self.current_state = self.state["IDLE]
    self.current_frame = 0

    self.image = self.animation_sets[self.current_state][self.current_frame]
    """
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
