import pygame
import random

class Settings:

    def __init__(self):
        """class to store all of the game's settings"""

        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))

        #background image
        self.screen_bg = pygame.transform.scale(pygame.image.load(
                    ('stars.png')), (self.screen_width, self.screen_height))
        
        #bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 5
        
        #alien bullet settings
        self.alien_bullets_allowed = 3
        self.alien_bullet_cooldown = 1000.0
        self.last_alien_shot = pygame.time.get_ticks()

        #alien settings
        self.fleet_drop_speed = 10

        #set default difficulty level
        self.difficulty_level = 'medium'

        #how quickly the game speeds up
        self.alien_speedup_scale = 1.2
        self.ship_speedup_scale = 1.2
        self.bullet_speedup_scale = 1.2
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings that change throughout the game"""
        if self.difficulty_level == 'easy':
            self.ship_speed = 3.0
            self.ship_limit = 4
            self.bullet_speed = 2.5
            self.alien_speed = 1.0
            self.alien_bullet_speed = random.randint(2, 4)
        elif self.difficulty_level == 'medium':
            self.ship_speed = 3.5
            self.ship_limit = 3
            self.bullet_speed = 3.0
            self.alien_speed = 2.0
            self.alien_bullet_speed = random.randint(3, 5)
        elif self.difficulty_level == 'hard':
            self.ship_speed = 4.0
            self.ship_limit = 2
            self.bullet_speed = 3.5
            self.alien_speed = 2.5
            self.alien_bullet_speed = random.randint(4, 6)

        #scoring settings
        self.alien_points = 50

        #fleet_direction of 1 represents right, -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.ship_speedup_scale
        self.bullet_speed *= self.bullet_speedup_scale
        if self.alien_speed <= 17.5:
            self.alien_speed *= self.alien_speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def set_difficulty(self, diff_setting):
        if diff_setting == 'easy':
            print('easy')
        elif diff_setting == 'medium':
            print('medium')
        elif diff_setting == 'hard':
            print('hard)')

    def draw_background(self):
        self.screen.blit(self.screen_bg, (0, 0))