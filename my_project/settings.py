class Settings:
    """Задаем настройки игры"""

    def __init__(self):
        """Иницилизируем настройки игры"""
        # Задаем параметры коробля
        self.ship_speed = 1.5
        # Параметры снаряда
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        self.bg_color = (230, 230, 230)
