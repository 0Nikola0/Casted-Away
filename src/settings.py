import pygame
from src.paths import *

# General
CAPTION = "Castaway"
FPS = 60
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (1200, 680)

# Layers
NUM_OF_LAYERS = 7

# COLORS
BLACK = pygame.color.THECOLORS["black"]
WHITE = pygame.color.THECOLORS["white"]
GRAY = pygame.color.THECOLORS["gray"]
BROWN = pygame.color.THECOLORS["brown"]
GREEN = pygame.color.THECOLORS["green"]

# ACTORS
ADULT_ACTOR_SIZE = 32, 32
ADULT_ACTOR_VELOCITY = 30

# Sprite sheets
SPRITES_SHEET_SPRITE_SIZE = (48, 48)

# GUI
# HELLO_BUTTON_POS, HELLO_BUTTON_SIZE = (50, 50), (100, 50)
# ### Need these to set limit to where the player can move
PANEL_POS, PANEL_SIZE = (1000, 100), (200, 300)
ACTOR_POS, ACTOR_SIZE = (1000, 0), (200, 100)
RESOURCE_POS, RESOURCE_SIZE = (225, 0), (150, 50)
EVENT_DESC_POS, EVENT_DES_SIZE = (0, SCREEN_HEIGHT - 100), (SCREEN_WIDTH, 100)

# GLOBAL SUPPLIES
FOOD_SUPPLY = 500
WATER_SUPPLY = 500

# Level borders
LEVEL_BORDERS_THICKNESS = 2

SHORTCUTS = {
    "FEED_SELECTED_ACTOR": pygame.K_f,
}

# IDs.
ALL_ID = {}


def get_id(object_, ids):
    """Returns unique integer

    Currently used for pymunk collisions.
    :type object_: reference to object that called method
    :type ids: set of IDs of class that called method
    """
    for new_id in range(10000000):  # infinity number
        if new_id not in ALL_ID:
            ALL_ID[new_id] = object_
            ids[new_id] = object_
            return new_id
    raise Exception(
        """
        Universe in danger! How it even possible? 
        Perhaps you created to many objects or did to many main_loop resets!
        """)


def unbind_id(id_, ids):
    """Remove id from all sets

    This method needs to be called only in sprite class kill() method
    :type id_: unique int
    :type ids: set of IDs of class that called method
    """
    assert id_ in ALL_ID, "This method needs to be called only in sprite class kill() method "
    del ALL_ID[id_]
    del ids[id_]


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
