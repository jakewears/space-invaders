import pygame
from pygame.sprite import Sprite
from si_settings import Settings

class AlienBullets(Sprite):
    def __init__(self, x, y):
        super().__init__()

        #alien bullet settings
        self.alien_bullet_width = 3
        self.alien_bullet_height = 10
        self.alien_bullet_color = (255, 0, 0)
        #self.alien_bullet_speed = 2.0

        self.rect = pygame.Rect(0, 0, self.alien_bullet_width, 
                                self.alien_bullet_height)
        
        self.rect.center = [x, y]

        self.y = float(self.rect.y)

    def update_alien_bullets(self, ai_game):
        """move the alien bullets"""
        self.settings = ai_game.settings
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y
    
    def draw_alien_bullets(self, ai_game):
        """draw the bullets to the screen"""
        self.screen = ai_game.screen
        pygame.draw.rect(self.screen, self.alien_bullet_color, self.rect)