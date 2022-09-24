import sys
import pygame
from pygame.sprite import Sprite


class StarSpace():

    width = 800
    height = 600

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Star Space')
        self.stars = pygame.sprite.Group()
        self._create_many_star()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill((230, 230, 230))
            self.stars.draw(self.screen)
            pygame.display.flip()

    def _create_many_star(self):
        star = Star(self)
        star_width, star_height = star.rect.size
        available_space_x = self.width
        number_aliens_x = available_space_x // 2
        available_space_y = (self.height)
        number_rows = available_space_y // (star_height)
        for row_number in range(number_rows):
            for star_number in range(number_aliens_x):
                self._create_star(star_number, row_number)

    def _create_star(self, alien_number, row_number):
        # Создание пришельца и размещение его в ряду.
        star = Star(self)
        star_width, star_height = star.rect.size
        star.x = star_width + 2 * star_width * alien_number
        star.rect.x = star.x
        star.rect.y = star.rect.height + 2 * star.rect.height * row_number
        self.stars.add(star)


class Star(Sprite):

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.image = pygame.image.load('star.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)



ss = StarSpace()
ss.run()