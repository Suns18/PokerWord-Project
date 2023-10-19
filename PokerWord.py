import pygame

#ประกาศใช้งาน
pygame.init
pygame.font.init()

#หัวข้อเกม
pygame.display.set_caption("PokerWord")

#ขนาดหน้าจอเกม
SCREEN_W = 1280
SCREEN_H = 720
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen_rect = screen.get_rect()

#กำหนดสี
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#นำภาพเข้า
background = pygame.image.load("assets/images/background.jpg")
background = pygame.transform.scale(background, (SCREEN_W, SCREEN_H))

#ข้อความ
type_front = pygame.font.SysFont("arial", 30)
mess_start = type_front.render("Start", True, BLACK)

#แสดงเกม
def main_menu():
    """Main Menu Screen"""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(background, (0, 0))
        pygame.draw.rect(background, WHITE, (screen_rect.centerx - 30, screen_rect.centery + 70, 55, 40))
        screen.blit(mess_start, (screen_rect.centerx - 30, screen_rect.centery + 70))
        pygame.display.update()
    pygame.quit()
main_menu()
