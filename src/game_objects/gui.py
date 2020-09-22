import pygame
import pygame_gui
from typing import Callable

from src import settings as s


class CommandPanel(pygame_gui.elements.UIPanel):
    def __init__(self, *args, **kwargs):
        super(CommandPanel, self).__init__(*args, **kwargs)
        self.manager = kwargs['manager']
        self.button_n = 0
        self.button_start_at = (20, 50)
        self.button_size = (150, 50)
        self.button_spacing = 20

    def add_button(self, name) -> pygame_gui.elements.UIButton:
        """Adds a button to the panel returns the created object"""
        position = (self.button_start_at[0],
                    self.button_start_at[1] + self.button_size[1] * self.button_n)

        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(position, self.button_size),
            text=name,
            container=self,
            manager=self.manager
        )
        self.button_n += 1

        return button


class GUI(pygame.sprite.Sprite):
    def __init__(self):

        super(GUI, self).__init__()
        self.image = pygame.Surface(s.SCREEN_SIZE, flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.manager = pygame_gui.UIManager(s.SCREEN_SIZE)

        self.buttons = []

        # TODO move these out into their own clases?
        # Ths is just a mockup, once the layout is nailed down we can
        # organize it better.

        self.panel = CommandPanel(
            relative_rect=pygame.Rect(s.PANEL_POS, s.PANEL_SIZE),
            manager=self.manager,
            starting_layer_height=0
        )

        self.event_description = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(s.EVENT_DESC_POS, s.EVENT_DES_SIZE),
            html_text='Event Description goes here',
            manager=self.manager,
        )

    def create_command_button(self, text, callback: Callable):
        """Add a button to the command panel and bind a callback to it."""
        self.buttons.append({'object': self.panel.add_button(text),
                             'callback': callback })

    def handle_event(self, event):
        """Handles USEREVENT events for pygame_gui events

        If the event is UI_BUTTON_PRESSED, iterate over all the buttons and
        call the bound function."""

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for button in self.buttons:
                    if event.ui_element == button['object']:
                        button['callback']()

        self.manager.process_events(event)

    def update(self, time_delta, *args):
        self.manager.update(time_delta)

        self.image.fill((0, 0, 0, 0))
        self.manager.draw_ui(self.image)
