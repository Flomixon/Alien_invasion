import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.play_button = Button(self, 'Easy', 0)
        self.normal_button = Button(self, 'Normal', 70)
        self.hard_button = Button(self, 'Hard', 140)
        pygame.mixer.pre_init(44100, -16, 1, 512)
        self.s_piu = pygame.mixer.Sound('piu.ogg')
        self.s_bom = pygame.mixer.Sound('bom.ogg')

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Отслеживание событий клавиатуры и мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки"""
        if not self.stats.game_active:
            if self.play_button.rect.collidepoint(mouse_pos):
                self.button_initialized()
                self.settings.difficulty_speed(0.5)
            elif self.normal_button.rect.collidepoint(mouse_pos):
                self.button_initialized()
            elif self.hard_button.rect.collidepoint(mouse_pos):
                self.button_initialized()
                self.settings.difficulty_speed(1.5)

    def button_initialized(self):
        # Сброс игровых настроек.
        self.settings.initialize_dynamic_settings()
        # Сброс игровой статистики.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Очистка списка снарядов и пришельцев.
        self.aliens.empty()
        self.bullets.empty()

        # Создание нового флота и размещение коробля в центре.
        self._create_fleet()
        self.ship.center_ship()
        # Указатель мыши скрывается
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key in (pygame.K_q, pygame.K_ESCAPE):
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            self.s_piu.play()
        elif event.key == pygame.K_p:
            self._check_play_button(True)

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание пришельца и вычисление количества пришельцев в ряду
        # Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота вторжения.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._crate_alien(alien_number, row_number)

    def _crate_alien(self, alien_number, row_number):
        # Создание пришельца и размещение его в ряду.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        """При каждом проходе цикла перерисовываем экран."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Вывод информации о счете.
        self.sb.show_score()
        # Кнопка Play отображается в том случае, если игра не активна.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обнавление снарядов и уничтажает старые снаряды."""
        # Обновление позиции снарядов.
        self.bullets.update()

        # Удаление старых снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # Проверка попаданий в пришельцев.
        self._check_bullet_alien_collisions()
        # Проверка все ли прищшельцы уничожены
        if not self.aliens:
            # Унчтожение существующих снарядов, повышение скорости и создание нового флота.
            self.bullets.empty()
            self._create_fleet()
            sleep(0.5)
            self.settings.increase_speed()
            # Увеличение уровня.
            self.stats.level += 1
            self.sb.prep_level()

    def _check_bullet_alien_collisions(self):
        """Обработка колизий снарядов с пришельцами."""
        # Удаление пришельцев и снарядов, учавствующих в коллизиях.
        # При попадании удалить снаряд и пришельца.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.s_bom.play()
            self.sb.prep_score()
            self.sb.check_high_score()

    def _update_aliens(self):
        """Обновление позиции всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()
        # Проверка коллизий "пришелец - корабля"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Реагирует на достижения края экрана пришельцем."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Обрабатывает столкновение коробля с пришельцем."""
        if self.stats.ships_left:
            # Уменьшение ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Очистка списка пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение коробля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Небольшая пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Проверка, добрался ли пришелец до низа экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break
    # Проверка коммитов


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
