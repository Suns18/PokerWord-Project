"""Card"""
import pygame
import game_ui

class SpecialCard():
    """SpecialCard"""
    def __init__(self, name, state):
        self.name = name
        self.image = pygame.image.load("assets/special_card/{}.png".format(name))
        self.state = state


class Card():
    """Normal Card"""
    def __init__(self, name, x, y, scale):
        """Init"""
        self.name = name
        self.card = game_ui.GameUI("assets/alphabet_card/{}_card.png".format(name.lower()), x, y, scale)


    def show(self, screen):
        self.card.draw(screen)