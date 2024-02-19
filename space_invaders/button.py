import pygame.font

class Button:
    """a class to build buttons for the game"""

    def __init__(self, ai_game, msg):
        """initialize button attributes"""
        self.screen = ai_game.settings.screen
        self.screen_rect = ai_game.screen.get_rect()

        #set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #the button message needs to be prepped only once
        self._prep_message(msg)

    def _prep_message(self, msg):
        """turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def _update_msg_position(self):
        """if the button has moved, the text needs to be moved as well"""
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """draw a blank button and then draw the message"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)