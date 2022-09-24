class Settings:
    """Класс для хранение всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует статические настройки игры."""
        # Параметры экрана
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        # Настройка корабля
        self.ship_limit = 3
        # Парметры снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3
        # Настройка пришельцев
        self.fleet_drop_speed = 10
        # Темп ускорения игры
        self.speedup_scale = 1.19
        # Увеличение стоимости пришельца в зависимости от сложности
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры"""
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 0.8
        # fleet_direction = 1 обозначает движение вправо, а -1 - влево.
        self.fleet_direction = 1
        # Подсчет очков.
        self.alien_points = 50

    def difficulty_speed(self, difficulty):
        """Увеличение настройки скорости и стоимости пришельцев."""
        self.ship_speed_factor *= difficulty
        self.alien_speed_factor *= difficulty
        self.bullet_speed_factor *= difficulty
        self.alien_points = int(self.alien_points * difficulty)

    def increase_speed(self):
        """Увеличивает настройки скорости."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.speedup_scale)
