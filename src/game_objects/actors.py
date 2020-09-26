from random import randint, uniform

import pygame
from pymunk.vec2d import Vec2d

import src.settings as s
from src.game_objects.pymunk_bodies import ActorRigidBody
from src.graphics import SpriteSheet
from src.game_objects.gui import console_print_event


class Actor(pygame.sprite.Sprite, ActorRigidBody):
    __ACTORS_IDS = {}

    def __init__(self, pos, sprite_sheets, sounds, space, name=None, health=100, food=100):
        self.id = s.get_id(self, Actor.__ACTORS_IDS)
        ActorRigidBody.__init__(self, pos, s.ADULT_ACTOR_SIZE, self.id, space)
        pygame.sprite.Sprite.__init__(self)

        self.sounds = {key: pygame.mixer.Sound(sound) for key, sound in sounds.items()}
        list(map(lambda sound: sound.set_volume(0.5), self.sounds.values()))  # hungry sounds are too noisy omg
        self.do_hungry_sound = True

        self.name = name or "Actor ID: " + str(self.id)
        self.health, self.food = health, food
        self.hungery = 0.08  # How fast the player gets hungry
        self.hunger_damage_rate = 0.1

        self.directionx, self.directiony = 0, 0
        self.vel = s.ADULT_ACTOR_VELOCITY

        self.target_position = None

        self.selected = False

        # self.image, self.rect, and animation
        animation_length = 4  # 4 images in 1 animation set
        shs = {key: SpriteSheet(value) for key, value in sprite_sheets.items()}
        self.animation_sets = [[shs[sh].get_image(i) for i in range(animation_length)] for sh in shs]
        self.state = {state_name: i for i, state_name in enumerate(shs)}

        self.animation_sets[self.state["HURT"]] = self.animation_sets[self.state["HURT"]][:2]

        self.current_state = self.state["IDLE"]
        self.current_frame = 0

        self.image = self.animation_sets[self.current_state][self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)

        self.anim_delay = 0.2
        self.time_in_frame = 0.0

        self.time_to_change_dir = 0.0
        self.dir_delay = 0.5

    def move_by_mouse(self, pos):
        self.target_position = s.flip_y(pos)

        # if pos[0] == int(self.body.position.x):
            # self.directionx = 0
        # elif pos[0] > int(self.body.position.x):
            # self.directionx = 1
        # else:
            # self.directionx = -1

        # current_y = s.flip_y(self.body.position.y)
        # if pos[1] == int(current_y):
            # self.directiony = 0
        # elif pos[1] < int(current_y):
            # self.directiony = 1
        # else:
            # self.directiony = -1

        #self.dir_delay = -1

        # self.move()

    def synchronize_rect_body(self):
        """Synchronizes player rect with pymunk player shape"""
        self.rect.center = s.flip_y(self.body.position)

    def do_task(self, task):
        """
        Actor moves towards the task
        If at task movement stops and actor starts 'doing the task'
        """
        pm_task_pos = s.flip_y(task.rect.center)
        task_delta = pm_task_pos - self.body.position
        if task_delta.get_length_sqrd() < self.vel ** 2:
            # Stop movement
            self.directionx, self.directiony = 0, 0
            self.current_state = 0
            # Start doing the task
            task.do_task()
        else:
            # TODO: Kind of dirty. Maybe rewrite later.
            to_close_for_move = 2
            fix_num = 5
            # x
            if pm_task_pos[0] > int(self.body.position.x):
                self.directionx = 1

                if task_delta[0] < to_close_for_move:
                    self.directionx //= fix_num
            elif pm_task_pos[0] < int(self.body.position.x):
                self.directionx = -1

                if task_delta[0] < to_close_for_move:
                    self.directionx //= fix_num
            else:
                self.directionx = 0

            # y
            if pm_task_pos[1] < int(self.body.position.y):
                self.directiony = -1

                if task_delta[1] < to_close_for_move:
                    self.directionx //= fix_num
            elif pm_task_pos[1] > int(self.body.position.y):
                self.directiony = 1

                if task_delta[1] < to_close_for_move:
                    self.directionx //= fix_num
            else:
                self.directiony = 0

            self.move()

    def update_directions(self, time_delta):
        """
        -1: Left / Up
        0: No movement
        1: Right / Down
        """
        self.time_to_change_dir += time_delta
        if self.time_to_change_dir > self.dir_delay:
            # So they walk random distances
            self.dir_delay = uniform(0.05, 0.5)

            self.directionx = randint(-1, 1)
            self.directiony = randint(-1, 1)
            self.time_to_change_dir = 0.0

        self.move()

    def move(self):
        self.control_body.velocity = Vec2d(self.vel * self.directionx, self.vel * self.directiony)

        if self.directionx == 0 and self.directiony == 0:
            self.current_state = 3
        else:
            self.current_state = 4 if self.directionx == 1 else 5

        if self.directiony != 0:
            self.get_hungry()

        if self.directionx != 0:
            self.get_hungry()

    def get_hungry(self):
        self.food -= self.hungery
        self.food = max(0, self.food)

    def starve(self):
        self.health -= self.hunger_damage_rate

    def switch_selection(self):
        if self.selected is False:
            self.sounds[f"SELECT{randint(1, 2)}"].play()
        self.selected = not self.selected

    def eat(self, amount):
        self.sounds["EAT"].play()
        self.food = (self.food + amount) if (self.food + amount) <= 100 else 100
        self.do_hungry_sound = True
        print(f"Actor.food = {self.food}")

    def update(self, time_delta, *args):
        self.time_in_frame += time_delta

        self.synchronize_rect_body()

        self.get_hungry()

        if self.food < 30:
            if self.do_hungry_sound is True:
                self.sounds["HUNGRY"].play()
                self.do_hungry_sound = False

        if self.food <= 0:
            self.starve()

        if self.health <= 0:
            console_print_event(f"{self.name} has died!")
            self.kill()

        for state in self.state.values():
            if self.current_state == state:
                self.image = self.animation_sets[self.current_state][self.current_frame]
                if self.time_in_frame > self.anim_delay:
                    # Actor moves by himself
                    # self.update_directions(time_delta)

                    # self.do_task(args[0])

                    self.current_frame = (self.current_frame + 1) if self.current_frame < 3 else 0
                    self.time_in_frame = 0

        # Handle targets
        if self.target_position is not None:
            target_delta = self.target_position - self.body.position
            if target_delta.get_length_sqrd() < self.vel ** 2:
                self.control_body.velocity = 0, 0
                self.current_state = 3
            else:

                # Left-right direction
                if self.target_position[0] > int(self.body.position.x):
                    dir_x = 1
                elif self.target_position[0] < int(self.body.position.x):
                    dir_x = -1
                else:
                    dir_x = 0

                # Up-down direction
                if self.target_position[1] < int(self.body.position.y):
                    dir_y = -1
                elif self.target_position[1] > int(self.body.position.y):
                    dir_y = 1
                else:
                    dir_y = 0

                # Set animation
                if dir_x == 0 and dir_y == 0:
                    self.current_state = 3
                else:
                    self.current_state = 4 if dir_x == 1 else 5

                dv = Vec2d(self.vel * dir_x, self.vel * dir_y)
                self.control_body.velocity = self.body.rotation_vector.cpvrotate(dv)

    def kill(self):
        """Clean up actor's pymunk stuff and remove the actor from all sprite groups"""
        s.unbind_id(self.shape.collision_type, Actor.__ACTORS_IDS)
        print(f"ID[{self.shape.collision_type}] was unbind")
        ActorRigidBody.kill(self)
        pygame.sprite.Sprite.kill(self)
