"""Game Menu"""
import pygame, sys
import game_ui
import button
import score
import random
import health_bar, card

pygame.init()

SCREEN_W = 1280
SCREEN_H = 896
SCALE = 4
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
screen_rect = screen.get_rect()

background_img = pygame.image.load("assets/images/game_background.png")
background = pygame.transform.scale(background_img, (SCREEN_W, SCREEN_H))

#HOVER
hover_img = pygame.image.load("assets/images/hover_button.png")
hover_special_card = pygame.image.load("assets/images/hover_special_card.png")
hover_atk = pygame.image.load("model/fight_button/hover_fight_button.png")

#INPUT BUTTON
input_img = pygame.image.load("model/fight_button/fight-button.png")
input_button = button.Button(input_img, 16 * SCALE + input_img.get_width(), SCREEN_H - 16 * SCALE - input_img.get_height(), 4, hover_atk)

#ENTER INPUT BUTTON
enter_img = pygame.image.load("assets/images/enter_button.png")
enter_button = button.Button(enter_img, screen_rect.centerx, screen_rect.centery + 16*SCALE, 3, hover_img)

#CLOSE BUTTON
close_img = pygame.image.load("assets/images/exit_button.png")
close_button = button.Button(close_img, screen_rect.centerx, screen_rect.centery, 3, hover_img)

#POPUP
popup = game_ui.GameUI("assets/images/popup.png", screen_rect.centerx - (48 * 5), screen_rect.centery - 90, 5)

player_health = health_bar.HealthBar(8 * SCALE, 16 * SCALE, 8, 1, 4, 50, False)
enemy_health = health_bar.HealthBar(screen_rect.centerx + 24 * SCALE, 16 * SCALE, 16, 1, 4, 100, False)
atk_count = 0

vs_show = game_ui.GameUI("assets/images/vs.png", screen_rect.centerx - (16 * SCALE), 8 * SCALE, SCALE)


def show_health():
    """Show player and enemy health"""
    player_health.draw(screen)
    vs_show.draw(screen)
    enemy_health.draw(screen)

    #test
    font = pygame.font.Font(None, 32)
    player_per = player_health.hp / player_health.max_hp * 100
    enemy_per = enemy_health.hp / enemy_health.max_hp * 100
    status = "player:{} ---- enemy:{} ---- sheild:{} ---- atk_count:{}".format(player_per, enemy_per, player_health.shield, atk_count)
    status_text = font.render(status, True, (255, 255, 255))
    screen.blit(status_text, (0,0))
 
def main_game():
    """main game"""
    base_font = pygame.font.Font(None, 32)
    word = ""
    input_active = False

    popup_active = False
    popup_message = ""

    global player_health, enemy_health, atk_count
    player_health.hp = player_health.max_hp
    enemy_health.hp = enemy_health.max_hp

    my_special_cards = []
    special_cards = ["holy_pizza_card", "holy_shield_card", "holy_damage_card"]

    used_word = []
    spam = False

    while True:
        for event in pygame.event.get():
            screen.blit(background, (0, 0))
            show_health()

            if popup_active:
                popup.draw(screen)
                text_surface = base_font.render(popup_message, True, (107, 68, 70))
                screen.blit(text_surface, (screen_rect.centerx - (text_surface.get_width()//2), screen_rect.centery - 60))
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
                special_button = button.Button(special_img, special_card_posx, special_card_posy, 2.5, hover_special_card)
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

            if input_button.draw(screen):
                input_active = True
            #input field
            card_scale = 2.5
            card_gap = 100
            if input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        word = word[:-1]
                    elif event.unicode.lower() in score.score and len(word) < 27:
                        word += event.unicode
                if len(word) > 12:
                    card_scale -= 0.1 * (len(word) - 12)
                    card_scale = max(card_scale, 1.6)
                    card_gap -= 5 * (len(word) - 12)
                    card_gap = max(card_gap, 45)
                card_posx = (screen_rect.centerx - (32*card_scale)//2) - ((card_gap//2) * (len(word) - 1))
                for char in word:
                    if char == '_':
                        char = 'underscore'
                    card_img = game_ui.GameUI("assets/alphabet_card/{}_card.png".format(char.lower()), card_posx, screen_rect.centery - 150, card_scale)
                    card_img.draw(screen)
                    card_posx += card_gap
                if enter_button.draw(screen):
                    attack = 0
                    attack_random = True
                    #เช็คคำ
                    if word in score.lstmethod or word in score.lstmethodimport:
                        for char in word:
                            attack += score.score[char]
                        if atk_count >= 1 and word in used_word:
                            atk_count = 0
                            spam = True
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
                                    player_health.hp = min(player_health.max_hp, player_health.hp + 10)
                                elif special_card.name == "holy_shield_card":
                                    player_health.shield = True
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
                            
                        #หมีตี
                        if player_health.shield:
                            player_health.shield = False
                        if enemy_health.hp <= 0:
                            print("You Win")
                        elif enemy_health.hp <= 20:
                            player_health.hp -= 10
                        elif enemy_health.hp <= 50:
                            player_health.hp -= 5
                        elif enemy_health.hp <= 100:
                            player_health.hp -= 3
                        if player_health.hp <= 0:
                            print("You Lose")
                    else:
                        popup_active = True
                        popup_message = "\"" + word + "\" is not a Python method."
                    word = ""
                    input_active = False
    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()