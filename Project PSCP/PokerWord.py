import pygame

#ประกาศใช้งาน
pygame.init
pygame.font.init()

#หัวข้อเกม
pygame.display.set_caption("PokerWord")

#ขนาดหน้าจอเกม
screen_W = 1280
screen_H = 720
screen = pygame.display.set_mode((screen_W, screen_H))
screen_rect = screen.get_rect()

#กำหนดสี
black = (0, 0, 0)
white = (255, 255, 255)

#นำภาพเข้า
background = pygame.image.load("Image/background.jpg")
background = pygame.transform.scale(background, (screen_W, screen_H))

#ข้อความ
type_front = pygame.font.SysFont("arial", 30)
mess_start = type_front.render("Start", True, black)

#แสดงเกม
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background, (0, 0))
    pygame.draw.rect(background, white, (screen_rect.centerx - 30, screen_rect.centery + 70, 55, 40))
    screen.blit(mess_start, (screen_rect.centerx - 30, screen_rect.centery + 70))
    pygame.display.update()
pygame.quit()