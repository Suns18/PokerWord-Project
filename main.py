import pygame
import button, game

#ประกาศใช้งาน
pygame.init
pygame.font.init()

#หัวข้อเกม
pygame.display.set_caption("PyFight")

#ขนาดหน้าจอเกม
SCREEN_W = 1280
SCREEN_H = 896
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen_rect = screen.get_rect()

#กำหนดสี
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#นำภาพเข้า
background_img = pygame.image.load("assets/images/menu_background.png")
background = pygame.transform.scale(background_img, (SCREEN_W, SCREEN_H))

#HOVER
hover_img = pygame.image.load("assets/images/hover_button.png")

#START
start_img = pygame.image.load("assets/images/start_button.png")
start_button = button.Button(start_img, screen_rect.centerx, screen_rect.centery, 5, hover_img)

#EXIT
exit_img = pygame.image.load("assets/images/exit_button.png")
exit_button = button.Button(exit_img, screen_rect.centerx, screen_rect.centery + 128, 5, hover_img)

#แสดงเกม
def main_menu():
    """Main Menu Screen"""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(background, (0, 0))
        if start_button.draw(screen):
            game.main_game()
        if exit_button.draw(screen):
            running = False
        
        pygame.display.update()
    pygame.quit()


main_menu()