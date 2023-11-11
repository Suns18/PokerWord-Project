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

#INPUT BUTTON
input_img = pygame.image.load("assets/images/start_button.png")
input_button = button.Button(input_img, 150, SCREEN_H - 100, 2, hover_img)

#ENTER INPUT BUTTON
enter_img = pygame.image.load("assets/images/enter_button.png")
enter_button = button.Button(enter_img, screen_rect.centerx, screen_rect.centery + 100, 2, hover_img)

#ATTACK BUTTON
atk_img = pygame.image.load("assets/images/enter_button.png")
atk_button = button.Button(atk_img, 1130, SCREEN_H - 100, 2, hover_img)

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
    status = "player:{} ---- enemy:{} ---- sheild:{} ---- atk_count:{}".format(player_health.hp, enemy_health.hp, player_health.shield, atk_count)
    status_text = font.render(status, True, (255, 255, 255))
    screen.blit(status_text, (0,0))
 
def main_game():
    """main game"""
    base_font = pygame.font.Font(None, 64)
    text_input = ""
    word = ""
    input_active = False

    my_special_cards = []
    special_cards = ["holy_pizza_card", "holy_shield_card", "holy_damage_card"]

    used_word = []
    spam = False

    while True:
        for event in pygame.event.get():
            screen.blit(background, (0, 0))
            show_health()

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
            if input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    elif event.unicode.isalpha():
                        text_input += event.unicode
                card_posx = (screen_rect.centerx - 40) - (50 * (len(word) - 1))
                word = text_input
                for char in word:
                    card_img = game_ui.GameUI("assets/alphabet_card/{}_card.png".format(char.lower()), card_posx, screen_rect.centery - 150, 2.5)
                    card_img.draw(screen)
                    card_posx += 100
                global enemy_health, player_health, atk_count
                if enter_button.draw(screen):
                    word = text_input
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
                        print("please input again")
                    word = ""
                    text_input = ""
                    input_active = False
    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
