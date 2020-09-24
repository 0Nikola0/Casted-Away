import pygame
from pymunk import Vec2d

from src.game_objects.actors import ActorAdult, TestActor
from src.game_objects.background import Background
from src.game_objects.floor import TestFloor
from src.game_objects.gui import GUI
from src.game_objects.level_borders import LevelBorders
from src.main_loop import MainLoop

import src.settings as s
from src.events import SWITCH_SCENE

from src.state import State


MENU = pygame.event.Event(SWITCH_SCENE, {'scene': 'menu'})
GAME = pygame.event.Event(SWITCH_SCENE, {'scene': 'game'})
TEST = pygame.event.Event(SWITCH_SCENE, {'scene': 'test'})


class Scene:
    """Handle creating, managing, and cleaning up sprites."""
    def __init__(self, main_loop):
        self.sprites = []
        self.main_loop = main_loop
        self.all = pygame.sprite.LayeredUpdates()

    def load(self):
        pass


class MenuScene(Scene):
    """The main Game Scene."""
    def __init__(self, *args):
        super().__init__(*args)

        self.GUI = GUI()
        self.main_loop.add_event_handler(self.GUI)
        self.GUI.create_command_button(
            "Game Scene", lambda: pygame.event.post(GAME))
        self.GUI.create_command_button(
            "Test Scene", lambda: pygame.event.post(TEST))
        self.GUI.create_command_button(
            "Quit Program", lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))

        self.all.add(Background(s.SCREEN_SIZE, s.GRAY), layer=0)
        self.all.add(self.GUI, layer=6)

        self.main_loop.drawing_layers[0].add(self.all)


class GameScene(Scene):
    """The main Game Scene."""
    def __init__(self, *args):
        super().__init__(*args)

        self.state = State()

        # Here, for the Quit button, we just post a QUIT event up to MainLoop
        self.GUI = GUI()
        self.GUI.create_command_button(
            "Quit to Menu", lambda: pygame.event.post(MENU))
        self.GUI.create_command_button(
            "Test Scene", lambda: pygame.event.post(TEST))
        self.GUI.create_command_button(
            "Log", lambda: self.GUI.console_println("I am a log."))

        # We are using the 'layer' parameter of the LayeredUpdates class which
        # acts the same as a Sprite Group.
        self.all.add(Background(s.SCREEN_SIZE, s.GRAY), layer=0)
        self.all.add(ActorAdult((200, 200), s.BOY_SPRITE_SHEETS, self.main_loop.space), layer=1)
        self.all.add(ActorAdult((200, 250), s.GIRL_SPRITE_SHEETS, self.main_loop.space), layer=1)
        self.all.add(self.GUI, layer=6)
        self.all.add(self.state, layer=0) # add state so that it gets updates
        self.main_loop.add_event_handler(self.GUI)

        # Stick it in one layer, the LayeredUpdates Group will take care of it
        # TODO maybe remove the layer code? Good idea
        self.main_loop.drawing_layers[0].add(self.all)


class TestScene(Scene):
    """This scene is used for testing code. Put your hacks and test here."""
    def __init__(self, *args):
        super().__init__(*args)
        self.GUI = None

        # These groups NOT for draw and update.
        self.background_group = pygame.sprite.Group()
        self.actors_group = pygame.sprite.Group()
        self.floor_group = pygame.sprite.Group()
        self.GUI_group = pygame.sprite.Group()
        self.__test_actors_group = pygame.sprite.Group()
        self.__test_positions = ((200, 200), (300, 300))

        # Not sprite groups
        self.level_borders = []

        # Collisions
        self.level_border_actor_collision = []

        self.create_sprites()
        self.create_buttons()

    def create_sprites(self):
        self.create_background()
        self.create_map()
        self.create_actors(self.__test_positions)
        self.create_GUI()
        # self.__create_test_actor()

        self.set_draw_order()

    def set_draw_order(self):
        """Determine order of drawing

        Sprites in index -1 group will be drawn upper all others.
        Vice versa for 0 index group – it will be background.
        """
        self.main_loop.drawing_layers[0].add(self.background_group)  # back (skies) layer
        self.main_loop.drawing_layers[1].add(self.floor_group)  # floors layer
        self.main_loop.drawing_layers[2].add()  # walls layer
        self.main_loop.drawing_layers[3].add(self.actors_group)  # actors layer
        self.main_loop.drawing_layers[-3].add(self.__test_actors_group)  # main actor (player) layer
        self.main_loop.drawing_layers[-2].add()  # before player (e.g. tree leaves or sheds)
        self.main_loop.drawing_layers[-1].add(self.GUI_group)  # gui layer

    def create_GUI(self):
        self.GUI = GUI()
        self.GUI_group.add(self.GUI)
        self.main_loop.add_event_handler(self.GUI)

    def create_buttons(self):
        self.GUI.create_command_button(
            "Plant", lambda: print("Pressed Plant"))
        self.GUI.create_command_button(
            "Harvest", lambda: print("Pressed Harvest"))
        self.GUI.create_command_button(
            "Rest", lambda: print("Pressed Rest"))
        self.GUI.create_command_button(
            "Quit to Menu", lambda: pygame.event.post(MENU))
        # We can clear the buttons if necessary e.g. for a New Game menu
        # self.GUI.clear_command_buttons()

    def create_background(self):
        b = Background(
            s.SCREEN_SIZE,
            s.GRAY,
        )
        self.background_group.add(b)

    def create_actors(self, positions):
        def add_actors_collisions():
            """Code block for all actors collisions"""
            lb_ids = list(map(lambda id_: id_.collision_type, *self.level_borders))  # ids of level borders
            for lb_id in lb_ids:
                self.level_border_actor_collision.append(self.main_loop.space.add_collision_handler(
                        lb_id,  # level border id
                        actor.shape.collision_type,  # current actor id
                    ))  # add collision handler
                self.level_border_actor_collision[-1].data["actor"] = actor  # add ref to actor to collision handler
                self.level_border_actor_collision[-1].begin = actor.change_direction  # collision handler's func

        for x, y in positions:
            actor = ActorAdult((x, y), s.WOMAN_SPRITE_SHEETS, self.main_loop.space)
            add_actors_collisions()
            self.actors_group.add(actor)

    def __create_test_actor(self):
        pos = (230, 250)
        __ta = TestActor(pos, s.OLD_MAN_SPRITE_SHEETS, self.main_loop.space)
        self.__test_actors_group.add(__ta)
        self.main_loop.mouse_handlers.append(__ta.handle_mouse_event)

    def create_map(self):
        topleft = 50, 50
        bottomright = 500, 300
        f = TestFloor(topleft, bottomright, s.BROWN)
        self.floor_group.add(f)

        p0 = Vec2d(topleft)
        p1 = p0 + Vec2d(bottomright)
        self.level_borders.append(LevelBorders(
            s.flip_y(p0),
            s.flip_y(p1),
            space=self.main_loop.space,
            d=s.LEVEL_BORDERS_THICKNESS).get_segments)
