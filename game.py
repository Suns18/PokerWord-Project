"""Game Menu"""
import pygame, sys

pygame.init

SCREEN_W = 1280
SCREEN_H = 896
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

background_img = pygame.image.load("assets/images/game_background.png")
background = pygame.transform.scale(background_img, (SCREEN_W, SCREEN_H))


def main_game():
    """main game"""
    while True:
        for event in pygame.event.get():
            screen.blit(background, (0, 0))
            pygame.display.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()