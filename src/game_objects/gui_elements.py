import pygame
import pygame_gui
from typing import Callable

from src import settings as s


class CallbackButton(pygame_gui.elements.UIButton):
    """Extend UIButton with a 'callback' field"""
    def __init__(self, callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback


class BarValue(pygame.sprite.Sprite):
    """This is simply a container for bar values.

    It is necessary because UIScreenSpaceHealthBar requires a sprite
    with hardcoded 'health_capacity' and 'current_health' properties."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.health_capacity = 100
        self.current_health = 20


class ActorPanel(pygame_gui.elements.UIPanel):
    """A Panel to display information about an Actor"""
    def __init__(self, *args, **kwargs):
        super(ActorPanel, self).__init__(*args, **kwargs)
        self.manager = kwargs['manager']

        # TODO these are test values, must be linked to real data
        self.actor_name = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 0), (100, 20)),
            text="John Doe",
            manager=self.manager,
            container=self)

        self.health_bar_value = BarValue()
        self.health_bar = pygame_gui.elements.UIScreenSpaceHealthBar(
            relative_rect=pygame.Rect((20, 20), (100, 20)),
            manager=self.manager,
            container=self)
        self.health_bar.set_sprite_to_monitor(self.health_bar_value)

        self.food_bar_value = BarValue()
        self.food_bar = pygame_gui.elements.UIScreenSpaceHealthBar(
            relative_rect=pygame.Rect((20, 40), (100, 20)),
            manager=self.manager,
            container=self)
        self.food_bar.set_sprite_to_monitor(self.food_bar_value)

        self.water_bar_value = BarValue()
        self.water_bar = pygame_gui.elements.UIScreenSpaceHealthBar(
            relative_rect=pygame.Rect((20, 60), (100, 20)),
            manager=self.manager,
            container=self)
        self.water_bar.set_sprite_to_monitor(self.water_bar_value)


class CommandPanel(pygame_gui.elements.UIPanel):
    """A Panel with buttons go give commands to our Actors"""
    def __init__(self, *args, **kwargs):
        super(CommandPanel, self).__init__(*args, **kwargs)
        self.manager = kwargs['manager']
        self.button_n = 0
        self.button_start_at = (20, 20)
        self.button_size = (150, 50)
        self.button_spacing = 20

    def add_button(self, name, callback=None) -> CallbackButton:
        """Adds a button to the panel returns the created object"""
        position = (self.button_start_at[0],
                    self.button_start_at[1] + self.button_size[1] * self.button_n)

        button = CallbackButton(
            callback=callback,
            relative_rect=pygame.Rect(position, self.button_size),
            text=name,
            container=self,
            manager=self.manager
        )
        self.button_n += 1

        return button

class Console():
    """A console you can print lines to, use .println(text) to add a line."""
    def __init__(self, relative_rect, manager):
        self.relative_rect = relative_rect
        self.manager = manager
        self.text = "Welcome."

        self.text_box = None

        self.__create_text_box(self.text)

    def __create_text_box(self, text):
        """Replace the old text box with new, this is the way it is done."""
        if self.text_box:
            self.text_box.kill()

        self.text_box = pygame_gui.elements.UITextBox(
            relative_rect=self.relative_rect,
            html_text=text,
            manager=self.manager,
        )

    def println(self, text):
        """Add a line to the console and recreate the text box."""
        self.text = text + '<br>' + self.text
        self.__create_text_box(self.text)
