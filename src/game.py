import pygame

from src.game_objects.actors import ActorAdult
from src.game_objects.background import Background
from src.game_objects.gui import GUI
from src.main_loop import MainLoop
import src.settings as s


class Game(MainLoop):
    def __init__(self):
        super(Game, self).__init__(s.CAPTION, s.SCREEN_SIZE, s.FPS)

        self.background = pygame.sprite.Group()
        self.actors = pygame.sprite.Group()
        self.GUI = None

        self.__test_positions = ((50, 50), (100, 50))

        self.create_sprites()

    def create_GUI(self):
        gui = GUI(self)
        self.GUI = gui
        self.add_event_handler(gui)

    def create_sprites(self):
        self.create_background()
        self.create_map()
        self.create_actors(self.__test_positions)
        self.create_GUI()
        self.sprite_groups = [self.background, self.actors, self.GUI]

    def create_background(self):
        b = Background(
            s.SCREEN_SIZE,
            s.GRAY,
        )
        self.background.add(b)

    def create_actors(self, positions):
        for x, y in positions:
            actor = ActorAdult((x, y), s.OLD_MAN_SPRITE_SHEETS)
            self.actors.add(actor)

    def create_map(self):
        pass

    def update(self):
        super(Game, self).update()


def main():
    Game().run()


if __name__ == "__main__":
    main()
