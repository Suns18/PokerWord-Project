"""Menu"""
import pygame
import game_ui, button

background_url = "assets/images/word_list.png"
main_font = "assets/fonts/bjg-pixel-brandon-james-greer.ttf"

class Menu():
    def __init__(self, x, y, scale, button_img, button_hover_img):
        """Init"""
        self.menu = game_ui.GameUI(background_url, x, y, scale)
        self.button = button.Button(button_img, self.menu.rect.right, y, scale * 0.75, button_hover_img)
    

    def show_word(self, screen, word_list):
        """Show word list"""
        font = pygame.font.Font(main_font, 8)
        pos_y = self.menu.rect.top + 16
        for word in word_list:
            show_word = font.render(word.lower(), True, (107, 68, 70))
            screen.blit(show_word, (self.menu.rect.left + 16, pos_y))
            pos_y += 16
    

    def show(self, screen, word_list):
        """Show Menu"""
        self.menu.draw(screen)
        self.show_word(screen, word_list)