import pygame
from src import settings as s


class Task(pygame.sprite.Sprite):
    def __init__(self, task_id: int,  increasement: float, pos, size):
        super(Task, self).__init__()
        """
        Harvesting = ID: 0
        Getting water = ID: 1
        Sleep / Eat / Drink = ID: 2
        """
        self.task_id = task_id
        self.increasement = increasement    # How much you gain from doing the task per loop
        self.rect = pygame.Rect(pos, size)

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.empty_image = pygame.Surface((0,0))
        self.outline_image = pygame.Surface((self.rect.width, self.rect.height), flags=pygame.SRCALPHA)
        pygame.draw.rect(self.outline_image, (255,255,255,255), (0,0,self.rect.w, self.rect.h), 2)

    def do_task(self):
        # Checks which ID the task is assigned and calls the corresponding function
        return {0: self.harvest, 1: self.get_water, 2: self.increase_actor_stats}.get(self.task_id)()

    def harvest(self):
        s.FOOD_SUPPLY += self.increasement
        return " harvested food."

    def get_water(self):
        s.WATER_SUPPLY += self.increasement
        return " got some water."

    # Same method can be used to increase each of the actor's stats eg Food status, Sleep status..
    # Right now just does a rest message
    def increase_actor_stats(self):
        # current = (current + self.increasement) if (current + self.increasement) <= 100 else 100
        # TODO doesnt actually rest
        return " has rested a bit."

    def show_border(self):
        self.image = self.outline_image

    def hide_border(self):
        self.image = self.empty_image
