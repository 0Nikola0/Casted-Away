import pygame
import pygame_gui
from typing import Callable

from src import settings as s
from src.game_objects.gui_elements import CallbackButton, BarValue, ActorPanel, CommandPanel


class GUI(pygame.sprite.Sprite):
    def __init__(self):

        super(GUI, self).__init__()
        self.image = pygame.Surface(s.SCREEN_SIZE, flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.manager = pygame_gui.UIManager(s.SCREEN_SIZE, s.THEME)

        self.all_buttons = []

        # TODO move these out into their own clases?
        # Ths is just a mockup, once the layout is nailed down we can
        # organize it better.

        self.actor_panel = ActorPanel(
            relative_rect=pygame.Rect(s.ACTOR_POS, s.ACTOR_SIZE),
            manager=self.manager,
            starting_layer_height=0
        )

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
        self.all_buttons.append(self.panel.add_button(text, callback))

    def clear_command_buttons(self):
        """Kills all buttons in the command panel"""
        for button in self.all_buttons:
            button.kill()

        self.all_buttons = []
        self.panel.button_n = 0

    def handle_event(self, event):
        """Handles USEREVENT events for pygame_gui events

        If the event is UI_BUTTON_PRESSED, iterate over all the buttons and
        call the bound function."""

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for button in self.all_buttons:
                    if event.ui_element == button:
                        button.callback()

        self.manager.process_events(event)

    def update(self, time_delta, *args):
        self.manager.update(time_delta)

        self.image.fill((0, 0, 0, 0))
        self.manager.draw_ui(self.image)
