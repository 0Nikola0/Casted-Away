import os

import pygame

CAPTION = "Castaway"
FPS = 60
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (800, 600)

# COLORS
BLACK = pygame.color.THECOLORS["black"]
WHITE = pygame.color.THECOLORS["white"]
GRAY = pygame.color.THECOLORS["gray"]

# ACTORS
ADULT_ACTOR_SIZE = 32, 32

# Paths (temporary)
ASSERTS_DIRECTORY = os.path.abspath("./assets")
IMGS_DIRECTORY = os.path.join(ASSERTS_DIRECTORY, "imgs")
ACTORS_DIRECTORY = os.path.join(IMGS_DIRECTORY, "actors")

SPRITES_SHEET_SPRITE_SIZE = (48, 48)

SPRITE_OLD_MAN_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "1 Old_man")
SPRITE_OLD_MAN_IDLE = os.path.join(SPRITE_OLD_MAN_DIRECTORY, "Old_man.png")
SPRITE_OLD_MAN_ATTACK = os.path.join(SPRITE_OLD_MAN_DIRECTORY, "Old_man_attack.png")

SPRITE_OLD_WOMAN_DIRECTORY = os.path.join(ACTORS_DIRECTORY, "2 Old_woman")
SPRITE_OLD_WOMAN_IDLE = os.path.join(SPRITE_OLD_WOMAN_DIRECTORY, "Old_woman.png")
SPRITE_OLD_WOMAN_ATTACK = os.path.join(SPRITE_OLD_WOMAN_DIRECTORY, "Old_woman_attack.png")

