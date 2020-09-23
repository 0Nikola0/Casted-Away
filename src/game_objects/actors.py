from random import randint, uniform

import pygame
import pymunk as pm
from pymunk import Vec2d

import src.settings as s
from src.graphics import SpriteSheet


class ActorAdult(pygame.sprite.Sprite):
    __ACTOR_ID = s.ADULT_ACTOR_COLLISION_TYPE
    assert __ACTOR_ID < 1000, "Invalid actor id. " \
                              "Perhaps you added too much objects or did too much Scene reset() calls."

    def __init__(self, pos, sprite_sheets, space):
        # pymunk stuff
        self.body = pm.Body(mass=1, moment=pm.inf, body_type=pm.Body.DYNAMIC)
        self.control_body = pm.Body(body_type=pm.Body.KINEMATIC)

        pm_x, pm_y = s.flip_y(pos)
        pm_size_x, pm_size_y = s.ADULT_ACTOR_SIZE

        self.body.position = pm_x + pm_size_x // 2, pm_y - pm_size_y // 2  # body.position == rect.center
        self.control_body.position = self.body.position

        self.shape = pm.Poly.create_box(self.body, s.ADULT_ACTOR_SIZE)

        self.shape.collision_type = ActorAdult.get_id()  # for collisions

        self.pivot = pm.PivotJoint(self.control_body, self.body, (0, 0), (0, 0))
        self.pivot.max_bias = 0  # disable joint correction
        self.pivot.max_force = 1000  # Emulate linear friction

        space.add(self.control_body, self.body, self.shape, self.pivot)

        # pygame stuff
        super(ActorAdult, self).__init__()

        self.health, self.food = 100, 100
        self.hungery = 0.2    # How fast the player gets hungry

        sh = {key: SpriteSheet(value) for key, value in sprite_sheets.items()}
        self.images = []
        for x in sh:
            self.images_temp = []
            for i in range(4):
                self.images_temp.append(sh[x].get_image(i))
            self.images.append(self.images_temp)
        # Just to reference what type self.image should be
        self.image = sh["IDLE"].get_image(0)
        pygame.transform.scale(self.image, s.ADULT_ACTOR_SIZE)

        self.rect = self.image.get_rect(topleft=pos)
        self.state = {
            "ATTACK": 0,    # We can use attack when harvesting crops
            "DEATH": 1,
            "HURT": 2,      # This is only 2 frames not 4 like the others, might create problems
            "IDLE": 3,
            "WALK": 4,
            "WALK-L": 5
        }
        self.current_state = 3
        self.anim_type = 0
        self.anim_delay = 0.2
        self.time_in_frame = 0.0

        self.directionx, self.directiony = 0, 0
        # self.vel = 5
        self.vel = s.ADULT_ACTOR_VELOCITY

        self.time_to_change_dir = 0.0
        self.dir_delay = 0.5

        self.target_position = None

    def synchronize_rect_body(self):
        """Synchronizes player rect with pymunk player shape"""
        self.rect.center = s.flip_y(self.body.position)

    def do_task(self, task):
        """
        Actor moves towards the task
        If at task movement stops and actor starts 'doing the task'
        """
        if self.rect.colliderect(task.rect):
            # Stop movement
            self.directionx, self.directiony = 0, 0
            self.current_state = 0
            # Start doing the task
            task.do_task()
        else:
            if self.rect.x > task.rect.x:
                self.directionx = -1
                self.current_state = 5
            elif self.rect.x < task.rect.x:
                self.directionx = 1
                self.current_state = 4
            else:
                self.directionx = 0
            if self.rect.y > task.rect.y:
                self.directiony = -1
            elif self.rect.y < task.rect.y:
                self.directiony = 1
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

            self.directionx = randint(-2, 1)
            self.directiony = randint(-2, 1)
            self.time_to_change_dir = 0.0

        self.move()

    def move(self):

        dv = Vec2d(self.vel * self.directionx, self.vel * self.directiony)
        self.control_body.velocity = self.body.rotation_vector.cpvrotate(dv)  # actual moving

        if self.directiony == 1:
            # Actor food gets lower if he moves
            self.food -= self.hungery
            if (self.rect.y + self.vel) < s.EVENT_DESC_POS[1]:
                self.current_state = 4
            else:
                # Change direction
                self.directiony = -1

        elif self.directiony == -1:
            self.food -= self.hungery
            if (self.rect.y - self.vel) > 0:
                self.current_state = 4
            else:
                self.directiony = 1

        else:
            self.directiony = 0
            self.current_state = 3

        if self.directionx == 1:
            self.food -= self.hungery
            # If it doesnt go out of the screen
            if (self.rect.x + self.vel) < s.PANEL_POS[0]:
                self.current_state = 4
            else:
                # Changing direction to opposite
                self.directionx = -1

        elif self.directionx == -1:
            self.food -= self.hungery
            if (self.rect.x - self.vel) > 0:
                self.current_state = 5
            else:
                self.directionx = 1

        else:
            self.directionx = 0
            self.current_state = 4 if (self.directiony == 1) or (self.directiony == -1) else 3

    def update(self, time_delta, *args):
        self.time_in_frame += time_delta

        self.synchronize_rect_body()

        for state in self.state.values():
            if self.current_state == state:
                self.image = self.images[self.current_state][self.anim_type]
                if self.time_in_frame > self.anim_delay:
                    # Actor moves by himself
                    self.update_directions(time_delta)

                    # self.do_task(args[0])

                    self.anim_type = (self.anim_type + 1) if self.anim_type < 3 else 0
                    self.time_in_frame = 0

    def change_direction(self, arbiter, space, data):
        """Change self directions and velocity to opposite ones

        Function what called by pymunk collision handler.
        Basically it's a static method but placed here for code
        grouping (actors collisions are built-in actors class).
        """
        assert data["actor"] is self, "Collision error. Collision data and self aren't match!"

        data["actor"].directionx = -data["actor"].directionx
        data["actor"].directiony = -data["actor"].directiony
        data["actor"].control_body.velocity = -data["actor"].control_body.velocity
        return True

    @staticmethod
    def get_id():
        # TODO: We have a limit in 100 IDs. Killed actors also occupy IDы although they no longer need them or even
        #  Scene resets devour free IDs. Needs to fix later, but for testing it's ok
        new_id = ActorAdult.__ACTOR_ID
        ActorAdult.__ACTOR_ID += 1
        return new_id


class TestActor(ActorAdult):
    """Test actor for physics tests"""
    def __init__(self, pos, sprite_sheets, space):
        # physics stuff
        super(TestActor, self).__init__(pos, sprite_sheets, space)
        self.shape.color = (255, 0, 0, 0)

        self.target_position = None

    def select_target(self, target_pos):
        self.target_position = s.flip_y(target_pos)

    def handle_mouse_event(self, ev, pos):
        if ev == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif ev == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif ev == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        pass

    def handle_mouse_down(self, pos):
        self.select_target(pos)

    def handle_mouse_up(self, pos):
        pass

    def update(self, time_delta, *args):
        super(TestActor, self).update(time_delta, *args)
        self.synchronize_rect_body()  # yes, need to call it twice :(

        if self.target_position is not None:

            target_delta = self.target_position - self.body.position
            if target_delta.get_length_sqrd() < self.vel ** 2:
                self.control_body.velocity = 0, 0
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

                dv = Vec2d(self.vel * dir_x, self.vel * dir_y)
                self.control_body.velocity = self.body.rotation_vector.cpvrotate(dv)
