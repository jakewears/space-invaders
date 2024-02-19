import pygame
import sys
from time import sleep
import json
from pathlib import Path
import random

from si_settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from alien_bullets import AlienBullets
from explosions import Explosions

class SpaceInvaders:
    """General class for elements and behaviors"""
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        
        #create an instance to store game statistics
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullet_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

        self._create_fleet()
        
        pygame.display.set_caption('Space Invaders')

        self.play_button = Button(self, "Play")

        self._make_difficulty_buttons()

        self.game_active = False

    def run_game(self):    
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._fire_alien_bullets()
                self._update_alien_bullets()
                self._check_fleet_edges()
                self._update_aliens()
                self.explosion_group.update()

            self._update_screen()
            self.clock.tick(60)

    def reset_game(self):
        self.game_active = True
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self._prep_all_scores()
        self.sb.prep_level()
        self.sb.prep_ships()

        #remove any remaining bullets & aliens
        self._reset_ammo()
        self.aliens.empty()

        #create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)

    def _prep_all_scores(self):
        self.sb.check_high_score()
        self.sb.prep_score()

    def _reset_ammo(self):
        self.bullets.empty()
        self.alien_bullet_group.empty()
        self.explosion_group.empty()

    def _make_difficulty_buttons(self):
        self.easy_button = Button(self, 'Easy')
        self.medium_button = Button(self, 'Medium')
        self.hard_button = Button(self, 'Hard')

        self.easy_button.rect.top = (
            self.play_button.rect.top + 1.5*self.play_button.rect.height)
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = (
            self.easy_button.rect.top + 1.5*self.easy_button.rect.height)
        self.medium_button._update_msg_position()

        self.hard_button.rect.top = (
            self.medium_button.rect.top + 1.5*self.medium_button.rect.height)
        self.hard_button._update_msg_position()

    def _check_difficulty_buttons(self, mouse_pos):
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked and not self.game_active:
            self.settings.difficulty_level = 'easy'
            self.settings.initialize_dynamic_settings()
            self.reset_game()

        elif medium_button_clicked and not self.game_active:
            self.settings.difficulty_level = 'medium'
            self.settings.initialize_dynamic_settings()
            self.reset_game()

        elif hard_button_clicked and not self.game_active:
            self.settings.difficulty_level = 'hard'
            self.settings.initialize_dynamic_settings()
            self.reset_game()

    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._close_game()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                    self._check_difficulty_buttons(mouse_pos)
 
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_q:
            self._close_game()
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key == pygame.K_p and not self.game_active:
            self.reset_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """start the game when the player click play"""
        self.button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if self.button_clicked and not self.game_active:
            self.reset_game()

    def _fire_bullet(self):
        """create a new bullet and add it to the bullets sprite group"""
        if self.game_active:
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)

    def _update_bullets(self):
        """updates bullet positions and removes old bullets"""
        #update bullet positions
        self.bullets.update()

        #remove old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """respond to bullet-alien collisions"""
        #check for any bullets that have hit aliens
        # if so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for bullets in collisions.keys():
                explosion = Explosions(bullets.rect.centerx, bullets.rect.centery)
                self.explosion_group.add(explosion)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self._prep_all_scores()
            self.start_new_level()

    #alien bullets
    def _fire_alien_bullets(self):
        if self.game_active:
            self.time_now = pygame.time.get_ticks()
            if len(self.alien_bullet_group) < self.settings.alien_bullets_allowed:
                if (self.time_now - self.settings.last_alien_shot > 
                    self.settings.alien_bullet_cooldown):
                    attacking_alien = random.choice(self.aliens.sprites())
                    new_alien_bullet = AlienBullets(attacking_alien.rect.centerx, 
                                                    attacking_alien.rect.bottom)
                    self.alien_bullet_group.add(new_alien_bullet)
                    self.settings.last_alien_shot = self.time_now

    def _update_alien_bullets(self):
        self.alien_bullet_group.update()

        for alien_bullet in self.alien_bullet_group.copy():
            alien_bullet.update_alien_bullets(self)
            self._check_alien_bullet_ship_collisions()
            if alien_bullet.rect.top > self.settings.screen_height:
                self.alien_bullet_group.remove(alien_bullet)

    def _check_alien_bullet_ship_collisions(self):
        """respond to collisions involving the ship and alien bullets"""
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullet_group):
            self._ship_hit()

    def start_new_level(self):
        if not self.aliens:
            #destroy existing bullets and create new fleet
            self._reset_ammo()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """update the positions of all aliens in the fleet"""
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _create_fleet(self):
        """create the fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size    

        current_x, current_y = alien_width, 100
        while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width - 1 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 1.5 * alien_width

            #finished a row;reset x value, and increment y value
            current_x = alien_width
            current_y += 1.5 * alien_height

    def _create_alien(self, x_position, y_position):        
        """create a new alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """respond appropriately if any aliens reach the edge of the screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """respond to the ship being hit by an alien"""
        #decrement ships left
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #get rid of any remaining bullets and aliens
            self._reset_ammo()
            self.aliens.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """check if any aliens reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _update_screen(self):

        #update background image
        self.settings.draw_background()

        #update bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for alien_bullet in self.alien_bullet_group.sprites():
            alien_bullet.draw_alien_bullets(self)

        #update ship
        self.ship.blitme() 
        self.aliens.draw(self.screen)
        self.explosion_group.draw(self.screen)

        self.sb.show_score()

        if not self.game_active:
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
            self.play_button.draw_button()

        pygame.display.flip()

    def _close_game(self):
        """save high score and exit"""
        saved_high_score = self.stats.get_saved_high_score()
        if self.stats.high_score > saved_high_score:
            path = Path('high_score.json')
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)

        sys.exit()
        
if __name__ == '__main__':
    ai = SpaceInvaders()
    ai.run_game()