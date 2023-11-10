"""Game UI"""
import pygame


class GameUI():
    """Game UI"""
    def __init__(self, image_url, pos_x, pos_y, scale):
        """Init"""
        image = pygame.image.load(image_url)
        width = image.get_width() * scale
        height = image.get_height() * scale
        self.image = pygame.transform.scale(image, (int(width), int(height)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.clicked = False


    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))