"""Game Menu"""
import pygame, sys
import game_ui

pygame.init

SCREEN_W = 1280
SCREEN_H = 896
SCALE = 4
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen_rect = screen.get_rect()

background_img = pygame.image.load("assets/images/game_background.png")
background = pygame.transform.scale(background_img, (SCREEN_W, SCREEN_H))


player_health = 30
enemy_health = 100

vs_text = pygame.image.load("assets/images/vs.png")
vs_show = game_ui.GameUI(vs_text, screen_rect.centerx - (16 * SCALE), 8 * SCALE, SCALE)


def show_health():
    """Show player and enemy health"""
    vs_show.draw(screen)
 
def main_game():
    """main game"""
    while True:
        for event in pygame.event.get():
            screen.blit(background, (0, 0))
            show_health()
            pygame.display.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

main_game()
