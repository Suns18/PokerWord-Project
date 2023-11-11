"""Card"""
import pygame

class SpecialCard():
    """Card"""
    def __init__(self, name, state):
        self.name = name
        self.image = pygame.image.load("assets/special_card/{}.png".format(name))
        self.state = state