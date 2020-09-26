import os
import pygame
import pymunk
import pymunk.pygame_util
from collections import defaultdict

from src.game_objects.tasks import Task


class MainLoop:
    """Display initialization and the main loop

    This class created to separate game-logic from mainloop. Its run method does all basic pygame stuff:
    handle events, update game status, and draw sprites to screen_surface.

    """
    def __init__(self, caption, screen_size, frame_rate, num_of_layers):
        # display-window top left corner always will be open in this coordinates (x=600; y=40)
        # os.environ['SDL_VIDEO_WINDOW_POS'] = f"{20},{20}"

        self.running = True

        # Create layers that determine draw order
        self.drawing_layers = [pygame.sprite.Group() for _ in range(num_of_layers)]

        pygame.init()
        self.surface = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(caption)

        self.frame_rate = frame_rate
        self.clock = pygame.time.Clock()
        self.time_delta = 0.0

        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        self.event_handlers = []

        self.update_hooks = []

        # physics stuff
        self.space = pymunk.Space()
        self.space.gravity = 0, 0

        # Pymunk test draw
        self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        self.is_prototyping_mode = False

        # Testing for tasks
        self.task01 = Task(0, 1.0, (73, 135), (140, 140))   # Harvest
        self.task02 = Task(1, 1.0, (540, 245), (60, 10))    # Get water

    def update(self):
        """Update game state

        self.all_sprites group contains all pygame.sprite.Sprite object in the game. Every main loop iteration
        this method use the update method of every sprite. So by this method, we can create animations.
        """
        for obj in self.update_hooks:
            obj.update(self.time_delta)

        for layer in self.drawing_layers:
            # self.task01 - just for testing
            layer.update(self.time_delta, self.task01)

    def draw(self):
        """Draw all sprites into screen

        self.all_sprites group contains all pygame.sprite.Sprite object in the game. Every main loop iteration
        this method blit all sprites to the displayed surface
        """
        for layer in self.drawing_layers:
            layer.draw(self.surface)

        # Testing
        self.task01.draw(self.surface)

    def handle_events(self):
        """Handle the player's inputs

        self.keydown_handlers, self.keyup_handlers, and self.mouse_handlers contain objects key (and mouse) handlers.
        So every time then we need out object to respond to player input, we need to add a handle_event method to its
        class and then add this handler to handlers containers.

        When game_handler capture an event it calls the conforming object handle method from self.keyup_handlers,
        self.keydown_handlers, or self.mouse_handlers with key as an argument in case of keyup-keydown event or
        mouse position with mouse button in case of mouse event.

        Then the object can update its state in reply to transmitted event (key, mouse move, or mouse button).
        """
        for event in pygame.event.get():
            for handler in self.event_handlers:
                handler(event)

            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.keyup_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def add_event_handler(self, obj):
        self.event_handlers.append(obj.handle_event)

    def add_up_down_key_handlers(self, obj, key):
        self.keydown_handlers[key].append(obj.handle_key_down)
        self.keyup_handlers[key].append(obj.handle_key_up)

    def add_update_hook(self, obj):
        self.update_hooks.append(obj)

    def del_update_hook(self, obj):
        self.update_hooks.remove(obj)

    def reset(self):
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        self.event_handlers = []
        self.update_hooks = []

        for group in self.drawing_layers:
            group.empty()

        # pymunk reset
        if self.space.shapes:
            for s in self.space.shapes:
                self.space.remove(s)
        if self.space.bodies:
            for b in self.space.bodies:
                self.space.remove(b)
        if self.space.constraints:
            for c in self.space.constraints:
                self.space.remove(c)

    def run(self):
        while self.running:

            self.handle_events()
            self.update()
            self.draw()

            if self.is_prototyping_mode is True:
                self.space.debug_draw(self.draw_options)

            pygame.display.update()

            self.time_delta = self.clock.tick(self.frame_rate) / 1000.0

            self.space.step(1 / self.frame_rate)  # pymunk-physics clock.tick
