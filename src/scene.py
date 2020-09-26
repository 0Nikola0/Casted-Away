import pygame
from pymunk.vec2d import Vec2d

from src.game_objects.actors import Actor
from src.game_objects.background import Background
from src.game_objects.floor import TestFloor
from src.game_objects.gui import GUI
from src.game_objects.level_borders import LevelBorders
from src.game_objects.selection_box import SelectionBox
from src.scenes.game_over import GameOver
from src.game_objects.gui import console_print_event
from src.game_objects.obstacles import Obstacle
from src.game_objects.tasks import Task
from src.game_objects.pymunk_bodies import ObstacleBody

import src.settings as s
from src.events import COMMAND, SWITCH_SCENE
from src.map import TiledMap

from src.state import State


FEED = pygame.event.Event(COMMAND, {'value': 'feed'})
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
                if pos[0] < s.PLAY_AREA[0] and pos[1] < s.PLAY_AREA[1]:
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

        # Tasks
        # Testing for tasks
        self.tasks = [
            Task(task_id=0, increasement=.0, pos=(73, 135), size=(140, 140)),   # Harvest
            Task(1, 1.0, (535, 240), (110, 20)),    # Get water (1)
            Task(1, 1.0, (625, 475), (33, 45)),     # Get water(
            Task(1, 1.0, (590, 510), (33, 45)),
            Task(1, 1.0, (560, 547), (33, 45)),               # 2)
            Task(2, 1.0, (40, 325), (100, 55)),     # Resting place by the crops
            Task(2, 1.0, (420, 497), (125, 80))     # Resting place by the river
        ]

        self.obstacle_bodies = []

        # Obstacles
        Obstacle.space = self.main_loop.space
        self.obstacles = [  # House
                        ((255, 96),(228, 222)),
                        # Garden fence
                        ((20, 116), (30, 190)),
                        ((20, 106), (235, 20)),
                        ((45, 300), (160, 20)),
                        ((235, 126), (15, 50)),
                        # Pond next to house
                        ((483, 160), (257, 94)),
                        # River
                        ((730, 160), (30, 240)),
                        ((705, 380), (30, 55)),
                        ((680, 420), (30, 60)),
                        ((645, 480), (33, 45)),
                        ((610, 515), (33, 45)),
                        ((580, 552), (33, 45)),
                        # Bottom of map
                        ((0, 565), (590, 20)),
                        # Right
                        ((0, 0), (20, 570)),
                        # Left trees
                        ((20, 390), (155, 178)),
                        # Middle bottom trees
                        ((325, 480), (80, 90)),
                        # Right trees
                        ((485, 387), (180, 100)),
                        ((610, 352), (65, 40)),
                        ((650, 250), (50, 60))
                        ]

        for obstacle in self.obstacles:
            self.obstacle_bodies.append(Obstacle(obstacle[0], obstacle[1], self.main_loop.space))

        self.all.add(self.state, layer=0)  # add state so that it gets updates
        self.all.add(self.map, layer=0)
        self.all.add(self.actors.sprites(), layer=3)
        self.all.add(self.GUI, layer=6)

        # TODO This is a hack; remove old layer code
        self.main_loop.drawing_layers[0].add(self.all)

    def create_actor(self, position) -> Actor:
        actor = Actor(position, s.OLD_MAN_SPRITE_SHEETS, s.OLD_MAN_SOUNDS, self.main_loop.space)

        # set up collisions
        # for obstacle_id in self.obstacle_ids.keys():
            # self.obstacle_actor_collision.append(self.main_loop.space.add_collision_handler(
                    # lb_id,  # level border id
                    # actor.shape.collision_type,  # current actor id
                # ))  # add collision handler
            # self.obstacle_actor_collision[-1].data["actor"] = actor  # add ref to actor to collision handler
            # self.obstacle_actor_collision[-1].begin = actor.change_direction  # collision handler's func

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
            actor.food = 5      # testing death
            actor.health = 5
