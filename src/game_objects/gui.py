import pygame
import pygame_gui
from src import settings as s


class GUI:
    def __init__(self, main_loop):

        self.main_loop = main_loop
        self.manager = pygame_gui.UIManager(s.SCREEN_SIZE)

        self.hello_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), (100, 50)),
            text='Say Hello',
            manager=self.manager
        )

    def handle_event(self, event):
        """Handles USEREVENT events for pygame_gui events"""
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.hello_button:
                    print('Hello World!')

        self.manager.process_events(event)

    def update(self):
        self.manager.update(self.main_loop.time_delta)

    def draw(self, surface):
        self.manager.draw_ui(surface)
