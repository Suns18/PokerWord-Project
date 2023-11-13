"""Character"""
import pygame


class Character():
    """Character Class"""
    def __init__(self, char_x, char_y, scale, sprites_url, hp_bar):
        self.x = char_x
        self.y = char_y
        self.scale = scale * 8
        self.sprites = sprites_url
        self.health = hp_bar
        self.rect = pygame.Rect((0, 0, 32 * self.scale, 32 * self.scale))
        self.rect.bottomleft = (char_x, char_y)
    
    def action_frame(self, action):
        sprite = pygame.image.load(self.sprites + "/{}.png".format(action))
        action_area = pygame.transform.scale(sprite, (self.scale, self.scale))
        return action_area

    def action(self, screen, action):
        screen.blit(self.action_frame(action), (self.x, self.y))
