import pygame

from src.main_loop import MainLoop
from src.scene import Scene, MenuScene, GameScene, TestScene
from src.events import SWITCH_SCENE

import src.settings as s


class Game(MainLoop):
    """Basically a manager for all the Scenes."""
    def __init__(self):
        super(Game, self).__init__(s.CAPTION, s.SCREEN_SIZE, s.FPS, s.NUM_OF_LAYERS)

        # We set up a Menu Scene, and let it fire the scene change events
        self.scene = MenuScene(self)
        self.add_event_handler(self)

    def handle_event(self, event):
        """Scans for scene change events, and changes scenes."""
        if event.type == SWITCH_SCENE:
            self.reset()

            # TODO Kind of dirty, we should put these in a dict in scene.py
            if event.scene == 'game':
                self.scene = GameScene(self)
            elif event.scene == 'menu':
                self.scene = MenuScene(self)
            elif event.scene == 'test':
                self.scene = TestScene(self)

            # We must re-add the handler as we have reset everything
            self.add_event_handler(self)
            self.scene.GUI.console_println("switched to scene: " + event.scene)

    def update(self):
        super(Game, self).update()


def main():
    Game().run()


if __name__ == "__main__":
    main()
