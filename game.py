"""Game Menu"""
import pygame, sys
import game_ui
import button

pygame.init

SCREEN_W = 1280
SCREEN_H = 896
SCALE = 4
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen_rect = screen.get_rect()

background_img = pygame.image.load("assets/images/game_background.png")
background = pygame.transform.scale(background_img, (SCREEN_W, SCREEN_H))

#HOVER
hover_img = pygame.image.load("assets/images/hover_button.png")

#INPUT
input_img = pygame.image.load("assets/images/start_button.png")
input_button = button.Button(input_img, 150, SCREEN_H - 100, 4, hover_img)

#ENTER INPUT
enter_img = pygame.image.load("assets/images/exit_button.png")
enter_button = button.Button(input_img, screen_rect.centerx, screen_rect.centery + 100, 4, hover_img)


#HOVER
hover_img = pygame.image.load("assets/images/hover_button.png")

#INPUT
input_img = pygame.image.load("assets/images/start_button.png")
input_button = button.Button(input_img, 150, SCREEN_H - 100, 4, hover_img)

#ENTER INPUT
enter_img = pygame.image.load("assets/images/exit_button.png")
enter_button = button.Button(input_img, screen_rect.centerx, screen_rect.centery + 100, 4, hover_img)



player_health = 30
enemy_health = 100

vs_show = game_ui.GameUI("assets/images/vs.png", screen_rect.centerx - (16 * SCALE), 8 * SCALE, SCALE)


def show_health():
    """Show player and enemy health"""
    vs_show.draw(screen)
 
def main_game():
    """main game"""
    base_font = pygame.font.Font(None, 64)
    text_input = ""
    text = ""
    input_active = False
    while True:
        for event in pygame.event.get():
            screen.blit(background, (0, 0))
            show_health()

            #input field
            text_surface = base_font.render(text_input, True, (255, 255, 255))
            screen.blit(text_surface, (screen_rect.centerx - 100, screen_rect.centery))
            if input_button.draw(screen):
                input_active = True
            if input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    elif event.unicode.isalpha() and len(text_input) < 10:
                        text_input += event.unicode
                if enter_button.draw(screen):
                    text = text_input
                    text_input = ""
                    input_active = False

            card_posx = (screen_rect.centerx - 40) - (50 * (len(text) - 1))
            #show card on screen
            for char in text:
                card_img = pygame.image.load("assets/alphabet_card/{}_card.png".format(char.lower()))
                card_img = pygame.transform.scale(card_img, (card_img.get_width() * 2.5, card_img.get_height() * 2.5))
                screen.blit(card_img, (card_posx, screen_rect.centery - 150))
                card_posx += 100

            pygame.display.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

main_game()
