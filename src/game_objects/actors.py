from random import randint, uniform

import pygame
import src.settings as s
from src.graphics import SpriteSheet


class ActorAdult(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_sheets):
        super(ActorAdult, self).__init__()

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
        self.vel = 5

        self.time_to_change_dir = 0.0
        self.dir_delay = 0.5

    def do_task(self, task):
        """
        Actor moves towards the task
        If at task movement stops and actor starts 'doing the task'
        """
        if self.rect.colliderect(task.rect):
            # Stop movement
            self.directionx, self.directiony = 0, 0
            self.current_state = 0
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

    # TODO Make IDLE to appear 50% more likely, so actors not in constant movement
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

            self.directionx = randint(-2, 2)
            self.directiony = randint(-2, 2)
            self.time_to_change_dir = 0.0

        self.move()

    # TODO Its when when directionx=0 directionsy=-1 (when moving straight down)
    def move(self):
        if self.directiony == 1:
            if (self.rect.y + self.vel) < s.EVENT_DESC_POS[1]:
                self.rect.y += self.vel
                self.current_state = 4
            else:
                # Change direction
                self.directiony *= -1

        elif self.directiony == -1:
            if (self.rect.y - self.vel) > 0:
                self.rect.y -= self.vel
                self.current_state = 4
            else:
                self.directiony *= -1

        else:
            self.directiony = 0
            self.current_state = 3

        if self.directionx == 1:
            # If it doesnt go out of the screen
            if (self.rect.x + self.vel) < s.PANEL_POS[0]:
                self.rect.x += self.vel
                self.current_state = 4
            else:
                # Changing direction to opposite
                self.directionx *= -1

        elif self.directionx == -1:
            if (self.rect.x - self.vel) > 0:
                self.rect.x -= self.vel
                self.current_state = 5
            else:
                self.directionx *= -1

        else:
            self.directionx = 0
            self.current_state = 4 if self.directiony is (1 or -1) else 3

    def update(self, time_delta, *args):
        self.time_in_frame += time_delta

        for state in self.state.values():
            if self.current_state == state:
                self.image = self.images[self.current_state][self.anim_type]
                if self.time_in_frame > self.anim_delay:
                    # Actor moves by himself
                    self.update_directions(time_delta)

                    # self.do_task(args[0])

                    self.anim_type = (self.anim_type + 1) if self.anim_type < 3 else 0
                    self.time_in_frame = 0


"""
    def update(self):
        self.image = self.images[self.state["WALK"]][self.anim_type]
        self.anim_type = (self.anim_type + 1) if self.anim_type < 3 else 0
"""


class TestActor(ActorAdult):
    """Test actor for physics tests"""
    def __init__(self, pos, sprite_sheets):
        super(TestActor, self).__init__(pos, sprite_sheets)
        self.target = None
        self.vel = 1

    def select_target(self, target_pos):
        self.target = target_pos

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

        if self.target is not None:
            tx, ty = self.target
            if self.rect.centerx < tx:
                self.rect.x += self.vel
            elif self.rect.centerx > tx:
                self.rect.x -= self.vel

            if self.rect.centery < ty:
                self.rect.y += self.vel
            elif self.rect.centery > ty:
                self.rect.y -= self.vel
