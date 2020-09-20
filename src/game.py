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
        self.actors = pygame.sprite.Group()

    def create_background(self):
        b = Background(
            s.SCREEN_SIZE,
            s.GRAY,
        )
        self.background.add(b)
        self.all_sprites.add(b)

    def create_actors(self, positions):
        positions = ((50, 50), (50, 100))  # for tests
        for x, y in positions:
            actor = Actor((x, y))
            self.actors.add(actor)
            self.all_sprites.add(actor)
