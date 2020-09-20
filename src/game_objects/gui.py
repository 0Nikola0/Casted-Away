import pygame
import pygame_gui
from src import settings as s


class GUI(pygame.sprite.Sprite):
    def __init__(self, main_loop):

        super(GUI, self).__init__()
        self.image = pygame.Surface((0, 0))
        # self.image = pygame.Surface(s.SCREEN_SIZE)
        self.rect = self.image.get_rect()

        self.main_loop = main_loop
        self.manager = pygame_gui.UIManager(s.SCREEN_SIZE)

        # TODO move these out into their own clases?
        # Ths is just a mockup, once the layout is nailed down we can
        # organize it better.
        self.popup = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((200, 50), (300, 300)),
            window_display_title='Popup',
            manager=self.manager
        )

        self.hello_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 50), (100, 50)),
            text='Say Hello',
            container=self.popup,
            manager=self.manager
        )

        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((600, 0),
                                      (200, 400)),
            manager=self.manager,
            starting_layer_height=0
        )

        self.event_description = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, s.SCREEN_HEIGHT - 200),
                                      (s.SCREEN_WIDTH, 200)),
            html_text='Event Description goes here',
            manager=self.manager,
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
