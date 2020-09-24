import pygame
from src.paths import *

# General
CAPTION = "Castaway"
FPS = 60
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (800, 600)

# Layers
NUM_OF_LAYERS = 7

# COLORS
BLACK = pygame.color.THECOLORS["black"]
WHITE = pygame.color.THECOLORS["white"]
GRAY = pygame.color.THECOLORS["gray"]
BROWN = pygame.color.THECOLORS["brown"]

# ACTORS
ADULT_ACTOR_SIZE = 32, 32
ADULT_ACTOR_VELOCITY = 30

# Sprite sheets
SPRITES_SHEET_SPRITE_SIZE = (48, 48)

# GUI
# HELLO_BUTTON_POS, HELLO_BUTTON_SIZE = (50, 50), (100, 50)
# ### Need these to set limit to where the player can move
PANEL_POS, PANEL_SIZE = (600, 100), (200, 300)
ACTOR_POS, ACTOR_SIZE = (600, 0), (200, 100)
EVENT_DESC_POS, EVENT_DES_SIZE = (0, SCREEN_HEIGHT - 200), (SCREEN_WIDTH, 200)

# GLOBAL SUPPLIES
FOOD_SUPPLY = 100
WATER_SUPPLY = 100

# Level borders
LEVEL_BORDERS_THICKNESS = 2

# IDs.
ALL_ID = set()


def get_id(ids):
    """Returns unique integer

    Currently used for pymunk collisions.
    :type ids: set of IDs of class that called method
    """
    for new_id in range(10000000):  # infinity number
        if new_id not in ALL_ID:
            ALL_ID.add(new_id)
            ids.add(new_id)
            return new_id
    else:
        assert True is False and False is True, "Universe in danger! How it even possible? " \
                                                "Do we have more than 10000000 objects?"


def unbind_id(id_, ids):
    """Remove id from all sets

    This method needs to be called only in sprite class kill() method
    :type id_: unique int
    :type ids: set of IDs of class that called method
    """
    assert id_ in ALL_ID, "This method needs to be called only in sprite class kill() method "
    ALL_ID.remove(id_)
    ids.remove(id_)


def flip_y(pos):
    """Convert pymunk physics to pygame coordinates

    In pymunk positive y is up
    """
    # if type(pos) is tuple or type(pos) is list:
    try:
        return pos[0], SCREEN_HEIGHT - pos[1]
    except TypeError:
        # else:
        y = pos
        return SCREEN_HEIGHT - y
