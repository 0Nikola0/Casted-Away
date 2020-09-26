import pygame
from pymunk import Vec2d

from src.game_objects.actors import Actor
from src.game_objects.background import Background
from src.game_objects.floor import TestFloor
from src.game_objects.gui import GUI
from src.game_objects.level_borders import LevelBorders
from src.game_objects.selection_box import SelectionBox
from src.game_objects.empty_sprite import EmptySprite
from src.main_loop import MainLoop
from src.scenes.game_over import GameOver
from src.game_objects.gui import console_print_event
from src.game_objects.obstacles import Obstacle

import src.settings as s
from src.events import COMMAND, SWITCH_SCENE
from src.map import TiledMap

from src.state import State


FEED = pygame.event.Event(COMMAND, {'value' : 'feed'})
MENU = pygame.event.Event(SWITCH_SCENE, {'scene': 'menu'})
GAME = pygame.event.Event(SWITCH_SCENE, {'scene': 'game'})
TEST = pygame.event.Event(SWITCH_SCENE, {'scene': 'test'})

# Layers
SELECTION_L = 5


class Scene:
    """Handle creating, managing, and cleaning up sprites."""
    def __init__(self, main_loop):
        self.main_loop = main_loop

        self.GUI = None
        self.all = pygame.sprite.LayeredUpdates()
        self.selected_actor = pygame.sprite.GroupSingle()
        self.selection_box = SelectionBox(s.GREEN)
        self.all.add(self.selection_box, layer=SELECTION_L)

        self.shortcuts = s.SHORTCUTS

        self.main_loop.mouse_handlers.append(self.handle_mouse_event)
        for key in self.shortcuts.values():
            self.main_loop.add_up_down_key_handlers(self, key)

    def load(self):
        pass

    def feed_selected_actor(self):
        if self.selected_actor.sprite is not None:
            if s.FOOD_SUPPLY > 15:
                self.selected_actor.sprite.eat(15)
                s.FOOD_SUPPLY -= 15
            else:
                console_print_event("Need more food!")

    def handle_key_down(self, key):
        pass

    def handle_key_up(self, key):
        if key == self.shortcuts["FEED_SELECTED_ACTOR"]:
            self.feed_selected_actor()

    def handle_mouse_event(self, ev, pos):
        if ev == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif ev == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
            # TODO this might not the best way to do it
            if self.selected_actor.sprite is not None:
                self.selected_actor.sprite.move_by_mouse(pos)
        elif ev == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        pass

    def handle_mouse_down(self, pos):
        pos = s.flip_y(pos)
        for shape in self.main_loop.space.shapes:
            dist, info = shape.point_query(pos)
            if dist < 0:
                clicked_object = self.main_loop.take_object_by_id(shape.collision_type)
                if isinstance(clicked_object, Actor):
                    actor = clicked_object

                    # Select
                    if len(self.selected_actor) == 0:
                        print(f"Actor with ID[{actor.id}] was selected")
                        actor.switch_selection()
                        self.selected_actor.add(actor)
                        self.GUI.select_actor(actor)

                        self.selection_box.bind_to(actor)

                    # Unselect
                    elif self.selected_actor.sprite == actor:
                        print(f"Actor with ID[{actor.id}] was unselected")
                        self.selected_actor.sprite.switch_selection()  # unselect actor
                        self.selected_actor.remove(self.selected_actor.sprite)
                        self.GUI.select_actor(None)

                        self.selection_box.reset()

                    # Unselect and Select
                    else:
                        self.selected_actor.sprite.switch_selection()
                        self.selected_actor.remove(self.selected_actor.sprite)
                        self.selected_actor.add(actor)
                        self.GUI.select_actor(actor)

                        self.selection_box.bind_to(actor)

    def handle_mouse_up(self, pos):
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

        self.main_loop.drawing_layers[1].add(self.all)


class GameScene(Scene):
    """The main Game Scene."""
    def __init__(self, *args):
        super().__init__(*args)

        self.level_borders_ids = {}
        self.level_border_actor_collision = []

        self.state = State()

        self.GUI = GUI()
        self.GUI.create_command_button(
            "Feed Actor", lambda: self.feed_selected_actor())
        self.GUI.create_command_button(
            "Quit", lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))

        self.main_loop.add_event_handler(self.GUI)
        self.main_loop.add_event_handler(self)

        self.main_loop.add_update_hook(self)

        self.map = TiledMap(s.MAP)

        self.actors = pygame.sprite.Group()
        self.actors.add(self.create_actor((200, 200)))
        self.actors.add(self.create_actor((200, 250)))

        # Obstacles
        self.obstacles = [  # House
                        Obstacle(pos=(255, 96), size=(228, 222)),
                        # Garden fence
                        Obstacle((20, 116), (30, 190)),
                        Obstacle((20, 106), (235, 20)),
                        Obstacle((45, 300), (160, 20)),
                        Obstacle((235, 126), (15, 50)),
                        # Pond next to house
                        Obstacle((483, 160), (257, 94)),
                        # River
                        Obstacle((730, 160), (30, 240)),
                        Obstacle((705, 380), (30, 55)),
                        Obstacle((680, 420), (30, 60)),
                        Obstacle((645, 480), (33, 45)),
                        Obstacle((610, 515), (33, 45)),
                        Obstacle((580, 552), (33, 45)),
                        # Bottom of map
                        Obstacle((0, 565), (590, 20)),
                        # Right
                        Obstacle((0, 0), (20, 570)),
                        # Left trees
                        Obstacle((20, 390), (155, 178)),
                        # Middle bottom trees
                        Obstacle((325, 480), (80, 90)),
                        # Right trees
                        Obstacle((485, 387), (180, 100)),
                        Obstacle((610, 352), (65, 40)),
                        Obstacle((650, 250), (50, 60))
                        ]

        self.all.add(self.state, layer=0)  # add state so that it gets updates
        self.all.add(self.map, layer=0)
        self.all.add(self.actors.sprites(), layer = 3)
        self.all.add(self.GUI, layer=6)

        # TODO This is a hack; remove old layer code
        self.main_loop.drawing_layers[0].add(self.all)

    def create_actor(self, position) -> Actor:
        actor = Actor(position, s.OLD_MAN_SPRITE_SHEETS, s.OLD_MAN_SOUNDS, self.main_loop.space)

        # set up collisions
        for lb_id in self.level_borders_ids.keys():
            self.level_border_actor_collision.append(self.main_loop.space.add_collision_handler(
                    lb_id,  # level border id
                    actor.shape.collision_type,  # current actor id
                ))  # add collision handler
            self.level_border_actor_collision[-1].data["actor"] = actor  # add ref to actor to collision handler
            self.level_border_actor_collision[-1].begin = actor.change_direction  # collision handler's func

        return actor

    def create_map(self) -> pygame.sprite.Sprite:
        """Create the map and return the floor Sprite"""
        topleft = 50, 50
        bottomright = 500, 300
        f = TestFloor(topleft, bottomright, s.BROWN)

        p0 = Vec2d(topleft)
        p1 = p0 + Vec2d(bottomright)
        self.level_borders_ids.update(
            LevelBorders(s.flip_y(p0), s.flip_y(p1),
                         space=self.main_loop.space,
                         d=s.LEVEL_BORDERS_THICKNESS).get_ids
        )

        return f

    def handle_event(self, event):
        if event.type == COMMAND:
            if event.value == 'feed':
                if self.selected_actor.sprite:
                    self.selected_actor.sprite.eat(25)

    def update(self, delta_time, *args):
        if len(self.actors) == 0:
            print("Game Over")
            self.main_loop.drawing_layers[0].add(GameOver())
            self.main_loop.del_update_hook(self)


class TestScene(GameScene):
    """This scene is used for testing code. Put your hacks and test here."""
    def __init__(self, *args):
        super().__init__(*args)

        self.test = pygame.sprite.LayeredUpdates()
        for actor in self.actors:
            actor.food = 5 #testing death
            actor.health = 5
