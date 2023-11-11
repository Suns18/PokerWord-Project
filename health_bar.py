"""Health Bar"""
import pygame

HP_IMG = pygame.image.load("assets/images/health_bar.png")

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


    def show_hp(self, hp_type):
        level = pygame.Surface((8, 8))
        level.blit(HP_IMG, (0, 0), ((8 * hp_type, 0, 8, 8)))
        level = pygame.transform.scale(level, (self.scale, self.scale))
        return level


    def draw(self, screen):
        hp_percent = self.hp / self.max_hp * 100
        grid_percent = 100 / (self.grid_width)
        for i in range(self.grid_width):
            hp_type = 0 if hp_percent >= grid_percent * (i + 1) else 4 if hp_percent < grid_percent * i else (int(grid_percent * (i + 1) - hp_percent) % 4)
            screen.blit(self.show_hp(hp_type), (self.x + i * self.scale, self.y))