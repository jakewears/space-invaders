import pygame
from pygame.sprite import Sprite

class Explosions(Sprite):
    """class representing explosion animations"""
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"explosion_images/exp{num}.png")
            img = pygame.transform.scale(img, (100,100))
            #add image to list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        self.explosion_speed = 4
        #update explosion speed
        self.counter += 1
        if self.counter >= self.explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is done, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= self.explosion_speed:
            self.kill()