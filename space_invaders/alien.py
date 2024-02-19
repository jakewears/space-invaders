import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """class to represent alien ships"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.alien = ai_game.aliens

        #load alien image and set its rect attribute
        self.image = pygame.image.load('Owl1.png')
        self.rect = self.image.get_rect()

        #start each new alien near the top left of the screen
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height 

        #store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """return True if the alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """move the alien left or right"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x