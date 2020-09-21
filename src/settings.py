import pygame
from src.paths import *

CAPTION = "Castaway"
FPS = 60
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) = (800, 600)

# Layers
NUM_OF_LAYERS = 7

# COLORS
BLACK = pygame.color.THECOLORS["black"]
WHITE = pygame.color.THECOLORS["white"]
GRAY = pygame.color.THECOLORS["gray"]

# ACTORS
ADULT_ACTOR_SIZE = 32, 32

# Sprite sheets
SPRITES_SHEET_SPRITE_SIZE = (48, 48)

# GUI
# HELLO_BUTTON_POS, HELLO_BUTTON_SIZE = (50, 50), (100, 50)
# ### Need these to set limit to where the player can move
PANEL_POS, PANEL_SIZE = (600, 0), (200, 400)
EVENT_DESC_POS, EVENT_DES_SIZE = (0, SCREEN_HEIGHT - 200), (SCREEN_WIDTH, 200)
