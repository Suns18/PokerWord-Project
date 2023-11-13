import pygame, sys
import button
import game_ui
import score
import random
import health_bar, card, menu, character

#ประกาศใช้งาน
pygame.init()
pygame.font.init()
pygame.mixer.init()

#หัวข้อเกม
pygame.display.set_caption("PyFight")

#ขนาดหน้าจอเกม
SCREEN_W = 1280
SCREEN_H = 896
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen_rect = screen.get_rect()

SCALE = 4

#กำหนดสี
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#SOUND
button_click_sound = pygame.mixer.Sound("assets/sounds/gameboy-pluck.ogg")
game_start_sound = pygame.mixer.Sound("assets/sounds/game-start.ogg")
game_win_sound = pygame.mixer.Sound("assets/sounds/winsquare.ogg")
game_lose_sound = pygame.mixer.Sound("assets/sounds/game-over.ogg")

button_click_sound.set_volume(0.5)
game_start_sound.set_volume(0.5)
game_win_sound.set_volume(0.6)
game_lose_sound.set_volume(0.4)

#นำภาพเข้า
background_img = pygame.image.load("assets/images/menu_background.png")
background = pygame.transform.scale(background_img, (SCREEN_W, SCREEN_H))

game_background_img = pygame.image.load("assets/images/game_bg.jpg")
game_background = pygame.transform.scale(game_background_img, (SCREEN_W, SCREEN_H))

#HOVER
hover_img = pygame.image.load("assets/images/hover_button.png")
hover_special_card = pygame.image.load("assets/images/hover_special_card.png")
hover_atk = pygame.image.load("model/fight_button/hover_fight_button.png")
hover_menu = pygame.image.load("assets/images/word_list_menu_hover.png")

#START
start_img = pygame.image.load("assets/images/start_button.png")
start_button = button.Button(start_img, screen_rect.centerx, screen_rect.centery, 5, hover_img, game_start_sound)

#EXIT
exit_img = pygame.image.load("assets/images/exit_button.png")
exit_button = button.Button(exit_img, screen_rect.centerx, screen_rect.centery + 128, 5, hover_img, button_click_sound)
exit_popup_button = button.Button(exit_img, screen_rect.centerx, screen_rect.centery, 3, hover_img, button_click_sound)

#INPUT BUTTON
input_img = pygame.image.load("model/fight_button/fight-button.png")
input_button = button.Button(input_img, 16 * SCALE + input_img.get_width(), SCREEN_H - 16 * SCALE - input_img.get_height(), 4, hover_atk, button_click_sound)

#ENTER INPUT BUTTON
enter_img = pygame.image.load("assets/images/enter_button.png")
enter_button = button.Button(enter_img, screen_rect.centerx, screen_rect.centery - 42*SCALE, 3, hover_img, button_click_sound)

#CLOSE MENU
close_menu_img = pygame.image.load("assets/images/close_button.png")

#WORD LIST
word_list_img = pygame.image.load("assets/images/word_list_menu.png")
word_list_button = button.Button(word_list_img, 8 * SCALE, 84 * SCALE, 3, hover_menu, button_click_sound)
word_list = menu.Menu(16 * SCALE, 72 * SCALE, 4, close_menu_img, hover_menu, button_click_sound)

#FONT
main_font = "assets/fonts/bjg-pixel-brandon-james-greer.ttf"

#POPUP
popup = game_ui.GameUI("assets/images/popup.png", screen_rect.centerx - (48 * 5), screen_rect.centery - 90, 5)

#CLOSE POPUP BUTTON
close_img = pygame.image.load("assets/images/close_button.png")
close_button = button.Button(close_img, (popup.rect.x + popup.image.get_width() - 8), popup.rect.y + 8, 2, hover_menu, button_click_sound)


player_health = health_bar.HealthBar(8 * SCALE, 16 * SCALE, 8, 1, 4, 50, False)
player = character.Character(64 * SCALE, 80 * SCALE, 32, "assets/character/player", player_health)

enemy_health = health_bar.HealthBar(screen_rect.centerx + 24 * SCALE, 16 * SCALE, 16, 1, 4, 100, False)
enemy = character.Character(160 * SCALE, 64 * SCALE, 40, "assets/character/bear", enemy_health)
atk_count = 0

vs_show = game_ui.GameUI("assets/images/vs.png", screen_rect.centerx - (48 * SCALE), 8 * SCALE, SCALE)


#แสดงเกม
def main_menu():
    """Main Menu Screen"""
    running = True
    pygame.mixer.music.load("assets/sounds/pixel-perfect.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1, fade_ms=1000)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(background, (0, 0))
        if start_button.draw(screen):
            main_game()
        if exit_button.draw(screen):
            running = False
        
        pygame.display.update()
    pygame.quit()




def show_health():
    """Show player and enemy health"""
    player.health.draw(screen)
    vs_show.draw(screen)
    enemy_health.draw(screen)



def main_game():
    """main game"""
    pygame.mixer.music.load("assets/sounds/man-is-he-mega-glbml.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(loops=-1, fade_ms=1000)
    word = ""
    input_active = False

    popup_active = False
    popup_message = ""

    global player, enemy_health, atk_count, last_update
    player.health.hp = player.health.max_hp
    enemy_health.hp = enemy_health.max_hp

    my_special_cards = []
    special_cards = ["holy_pizza_card", "holy_shield_card", "holy_damage_card"]

    used_word = []
    spam = False

    show_word_list = False

    bear_phase = "phase1"

    game_end = False

    while True:
        for event in pygame.event.get():
            screen.blit(game_background, (0, 0))
            show_health()
            player.action(screen, "idle")
            enemy.action(screen, bear_phase)
            if word_list_button.draw(screen):
                show_word_list = True

            if show_word_list:
                word_list.show(screen, used_word)
                if word_list.button.draw(screen):
                    show_word_list = False

            if popup_active:
                popup.draw(screen)
                font_size = 32
                base_font = pygame.font.Font(main_font, font_size)
                text_surface = base_font.render(popup_message, True, (107, 68, 70))
                while text_surface.get_width() > popup.image.get_width() - 10:
                    font_size -= 1
                    base_font = pygame.font.Font(main_font, font_size)
                    text_surface = base_font.render(popup_message, True, (107, 68, 70))
                screen.blit(text_surface, (screen_rect.centerx - (text_surface.get_width()//2), (popup.rect.y + max(0, (popup.image.get_height()//2) - text_surface.get_height()) + 10)))
                if game_end:
                    if exit_popup_button.draw(screen):
                        main_menu()
                else:
                    if close_button.draw(screen) or input_active == True:
                        popup_active = False

            special_card_posx = screen_rect.centerx - (75 * (len(my_special_cards) - 1))
            #show special card on screen
            for special_card in my_special_cards:
                special_img = special_card.image
                special_card_posy = screen_rect.centery + 325
                #เช็คการใช้ special card
                if special_card.state == True:
                    special_card_posy -= 50
                special_button = button.Button(special_img, special_card_posx, special_card_posy, 2.5, hover_special_card, button_click_sound)
                #กดใช้ special card
                if special_button.draw(screen):
                    if special_card.state == True:
                        """กดซ้ำ กลับ True เป็น False"""
                        special_card.state = False
                    else:
                        for icard in my_special_cards:
                            icard.state = False
                        special_card.state = True
                special_card_posx += 150

            if input_button.draw(screen) and not game_end:
                input_active = True
            #input field
            card_scale = 2.5
            card_gap = 100
            if input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        word = word[:-1]
                    elif event.unicode.lower() in score.score and len(word) < 27:
                        word += event.unicode.lower()
                if len(word) > 12:
                    card_scale -= 0.1 * (len(word) - 12)
                    card_scale = max(card_scale, 1.6)
                    card_gap -= 5 * (len(word) - 12)
                    card_gap = max(card_gap, 45)
                card_posx = (screen_rect.centerx - (32*card_scale)//2) - ((card_gap//2) * (len(word) - 1))
                for char in word:
                    if char == '_':
                        char = 'underscore'
                    card_img = game_ui.GameUI("assets/alphabet_card/{}_card.png".format(char.lower()), card_posx, screen_rect.centery - 300, card_scale)
                    card_img.draw(screen)
                    card_posx += card_gap
                if enter_button.draw(screen):
                    attack = 0
                    attack_random = True
                    #เช็คคำ
                    if word in score.lstmethod or word in score.lstmethodimport:
                        for char in word:
                            attack += score.score[char]
                        if word in used_word:
                            atk_count = 0
                            spam = True
                            popup_active = True
                            popup_message = "This word is used, your atk damage is reduced"
                        else:
                            used_word.append(word)
                            atk_count += 1

                        #ได้ special card
                        if atk_count % 3 == 0 and atk_count != 0:
                            card_increase = random.choice(special_cards)
                            my_special_cards.append(card.SpecialCard(card_increase, False))

                        #ใช้ของ
                        for special_card in my_special_cards:
                            if special_card.state == True:
                                if special_card.name == "holy_pizza_card":
                                    player.health.hp = min(player.health.max_hp, player.health.hp + 10)
                                elif special_card.name == "holy_shield_card":
                                    player.health.shield = True
                                elif special_card.name == "holy_damage_card":
                                    attack_random = False
                                my_special_cards.remove(special_card)

                            
                        #เราตี
                        if not attack_random and not spam:
                            enemy_health.hp -= attack
                        elif not attack_random and spam:
                            enemy_health.hp -= 2
                            spam = False
                        elif attack_random and spam:
                            enemy_health.hp -= 1
                            spam = False
                        elif attack_random and not spam:
                            enemy_health.hp -= int(random.uniform(attack*0.2, attack))
                        enemy.action(screen, "damaged")
                            
                        #หมีตี
                        if enemy_health.hp <= 0:
                            popup_active = True
                            popup_message = "You Win!!!"
                            bear_phase = "dead"
                            pygame.mixer.music.unload()
                            game_win_sound.play()
                            game_end = True
                        if player.health.shield == False:
                            player.action(screen, "damaged")
                        if player.health.shield:
                            player.health.shield = False
                        elif enemy_health.hp <= 20:
                            player.health.hp -= 10
                            bear_phase = "phase3"
                        elif enemy_health.hp <= 50:
                            player.health.hp -= 5
                            bear_phase = "phase2"
                        elif enemy_health.hp <= 100:
                            player.health.hp -= 3
                            bear_phase = "phase1"
                        if player.health.hp <= 0:
                            popup_active = True
                            popup_message = "You Lose!!!"
                            pygame.mixer.music.unload()
                            game_lose_sound.play()
                            game_end = True
                    else:
                        popup_active = True
                        popup_message = "\"" + word + "\" is not a Python method."
                    word = ""
                    input_active = False
    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

main_menu()
