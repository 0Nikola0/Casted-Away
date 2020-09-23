import pygame

from src.main_loop import MainLoop
from src.scene import Scene, GameScene, TestScene

import src.settings as s


class Game(MainLoop):
    """Basically a manager for all the Scenes."""
    def __init__(self):
        super(Game, self).__init__(s.CAPTION, s.SCREEN_SIZE, s.FPS, s.NUM_OF_LAYERS)

        self.scene = TestScene(self)
        self.reset()
        self.scene = GameScene(self)
        # self.reset() # This will clear the scene so another can take it's place

    def update(self):
        super(Game, self).update()

def main():
    Game().run()


if __name__ == "__main__":
    main()
