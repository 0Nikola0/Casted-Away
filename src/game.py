# import src.gui_test
import pygame

from src.graphics import SpriteSheet
from src.main_loop import MainLoop
from src.game_objects.actors import ActorAdult
from src.game_objects.background import Background
import src.settings as s


class Game(MainLoop):
    def __init__(self):
        super(Game, self).__init__(s.CAPTION, s.SCREEN_SIZE, s.FPS)

        self.background = pygame.sprite.Group()
        self.actors = pygame.sprite.Group()

        self.__test_positions = ((50, 50), (100, 50))

        self.create_sprites()

    def create_sprites(self):
        self.create_background()
        self.create_map()
        self.create_actors(self.__test_positions)

    def create_background(self):
        b = Background(
            s.SCREEN_SIZE,
            s.GRAY,
        )
        self.background.add(b)
        self.all_sprites.add(b)

    def create_actors(self, positions):
        # __img = "./assets/imgs/actors/1 Old_man/Old_man.png"  # temporary for tests
        for x, y in positions:
            actor = ActorAdult((x, y), "0")
            self.actors.add(actor)
            self.all_sprites.add(actor)

    def create_map(self):
        pass

    def update(self):
        super(Game, self).update()


def main():
    Game().run()


if __name__ == "__main__":
    main()
