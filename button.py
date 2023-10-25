import pygame
class Button():
    """Class for button"""
    def __init__(self, image, pos_x, pos_y, scale, hover):
        """Init"""
        #button
        width = image.get_width() * scale
        height = image.get_height() * scale
        self.image = pygame.transform.scale(image, (int(width), int(height)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x - width//2, pos_y - height//2)
        self.clicked = False

        #hover
        width_hover = hover.get_width() * scale
        height_hover = hover.get_height() * scale
        self.hover = pygame.transform.scale(hover, (int(width_hover), int(height_hover)))
        self.hover_rect = self.hover.get_rect()
        self.hover_rect.topleft = (self.rect.x - (3 * scale), self.rect.y - (3 * scale))

    def draw(self, screen):
        """Draw button on screen"""
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            screen.blit(self.hover, (self.hover_rect.x, self.hover_rect.y))
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = True
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action