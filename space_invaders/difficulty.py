import pygame.font

class Difficulty:
    """class representing buttons for various difficulties in game"""

    def __init__(self, ai_game, easy, medium, hard):
        self.screen = ai_game.settings.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.width, self.height = 100, 30
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.easy_rect = pygame.Rect(0, 0, self.width, self.height)
        self.medium_rect = pygame.Rect(0, 0, self.width, self.height)
        self.hard_rect = pygame.Rect(0, 0, self.width, self.height)

        self.easy_rect.bottomleft = self.screen_rect.bottomleft
        self.medium_rect.bottom = self.screen_rect.bottom
        self.hard_rect.bottomright = self.screen_rect.bottomright

        self._prep_difficulties(easy, medium, hard)

    def _prep_difficulties(self, easy, medium, hard):
        self.easy_image = self.font.render(easy, True, self.text_color, self.button_color)
        self.medium_image = self.font.render(medium, True, self.text_color, self.button_color)
        self.hard_image = self.font.render(hard, True, self.text_color, self.button_color)

        self.easy_image_rect = self.easy_image.get_rect()
        self.medium_image_rect = self.medium_image.get_rect()
        self.hard_image_rect = self.hard_image.get_rect()

        self.easy_image_rect.center, self.medium_image_rect.center, self.hard_image_rect.center = self.easy_rect.center, self.medium_rect.center, self.hard_rect.center

    def draw_buttons(self):
        self.screen.fill(self.button_color, (self.easy_rect, self.medium_rect, self.hard_rect))
        self.screen.blit((self.easy_image, self.medium_image, self.hard_image), (self.easy_image_rect, self.medium_image_rect, self.hard_image_rect))