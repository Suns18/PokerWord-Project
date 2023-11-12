"""Health Bar"""
import pygame
import math

HP_IMG = pygame.image.load("assets/images/health_bar.png")
NUMBER_IMG = pygame.image.load("assets/images/health_number.png")

class HealthBar():
    """HealthBar"""
    def __init__(self, x, y, grid_width, grid_height, scale, max_hp, shield):
        """Init"""
        self.x = x
        self.y = y
        self.scale = scale * 8
        self.grid_width = grid_width
        self.width = grid_width * self.scale
        self.height = grid_height * self.scale
        self.hp = max_hp
        self.max_hp = max_hp
        self.shield = shield


    def show_hp_level(self, hp_type):
        level = pygame.Surface((8, 8))
        level.blit(HP_IMG, (0, 0), ((8 * hp_type, 0, 8, 8)))
        level = pygame.transform.scale(level, (self.scale, self.scale))
        return level


    def show_hp_number(self, num):
        """Return Number png"""
        number = pygame.Surface((8, 8), pygame.SRCALPHA)
        number.blit(NUMBER_IMG, (0, 0), ((8 * num, 0, 8, 8)))
        number = pygame.transform.scale(number, (self.scale, self.scale))
        return number


    def draw_num(self, screen):
        """Draw HP Number"""
        hp_text = str(max(0, self.hp))
        for i in range(len(hp_text)):
            digit = hp_text[i]
            screen.blit(self.show_hp_number(int(digit)), (self.x + i * self.scale, self.y - self.scale - 2))


    def draw_bar(self, screen):
        """Draw HP bar"""
        hp_percent = self.hp / self.max_hp * 100
        grid_percent = 100 / (self.grid_width)
        for i in range(1, self.grid_width + 1):
            hp_type = 0 if hp_percent >= grid_percent * i else 4 if hp_percent < grid_percent * (i - 1) else 4 - math.floor((grid_percent * i - hp_percent) / grid_percent * 0.25)
            screen.blit(self.show_hp_level(hp_type), (self.x + (i-1) * self.scale, self.y))

    def draw(self, screen):
        self.draw_bar(screen)
        self.draw_num(screen)