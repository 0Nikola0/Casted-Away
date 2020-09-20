# import src.gui_test
import pygame
from src.main_loop import MainLoop
from src.game_objects.actors import Actor
from src.game_objects.background import Background
import src.settings as s


class Game(MainLoop):
    def __init__(self):
        super(Game, self).__init__(s.CAPTION, s.SCREEN_SIZE, s.FPS)

        self.background = pygame.sprite.Group()

    def create_background(self):
        self.background.add(Background(
            s.SCREEN_SIZE,
            s.GRAY
        ))

    def create_actors(self, positions):
        actors = []
        for i in positions:
            actors.append()
