"""Game Menu"""
import pygame, sys
import game_ui
import button
import score
import random
import health_bar

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

#INPUT BUTTON
input_img = pygame.image.load("assets/images/start_button.png")
input_button = button.Button(input_img, 150, SCREEN_H - 100, 4, hover_img)

#ENTER INPUT BUTTON
enter_img = pygame.image.load("assets/images/enter_button.png")
enter_button = button.Button(enter_img, screen_rect.centerx, screen_rect.centery + 100, 4, hover_img)

#ATTACK BUTTON
atk_img = pygame.image.load("assets/images/enter_button.png")
atk_button = button.Button(atk_img, 1130, SCREEN_H - 100, 4, hover_img)

player_health = health_bar.HealthBar(8 * SCALE, 8 * SCALE, 6, 1, 4, 30)
enemy_health = 100
shield = 0
atk_count = 0


vs_show = game_ui.GameUI("assets/images/vs.png", screen_rect.centerx - (16 * SCALE), 8 * SCALE, SCALE)


def show_health():
    """Show player and enemy health"""
    vs_show.draw(screen)

    #test
    font = pygame.font.Font(None, 32)
    status = "player:{} ---- enemy:{} ---- sheild:{} ---- atk_count:{}".format(player_health.hp, enemy_health, shield, atk_count)
    status_text = font.render(status, True, (255, 255, 255))
    screen.blit(status_text, (0,0))
 
def main_game():
    """main game"""
    base_font = pygame.font.Font(None, 64)
    text_input = ""
    word = ""
    input_active = False

    holy_pizza_card = False
    holy_shield_card = False
    holy_damage_card = False
    my_special_cards = ["holy_shield_card", "holy_shield_card", "holy_shield_card"]
    special_cards = ["holy_pizza_card", "holy_shield_card", "holy_damage_card"]

    used_word = []
    spam = False

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
                    word = text_input
                    text_input = ""
                    input_active = False

            card_posx = (screen_rect.centerx - 40) - (50 * (len(word) - 1))
            special_card_posx = screen_rect.centerx - (75 * (len(my_special_cards) - 1))

            #show input card on screen
            for char in word:
                card_img = game_ui.GameUI("assets/alphabet_card/{}_card.png".format(char.lower()), card_posx, screen_rect.centery - 150, 2.5)
                card_img.draw(screen)
                card_posx += 100
            #show special card on screen
            for special_card in my_special_cards:
                special_img = pygame.image.load("assets/special_card/{}.png".format(special_card))
                special_card_posy = screen_rect.centery + 325
                #เช็คการใช้ special card
                if (holy_pizza_card and special_card == "holy_pizza_card") or (holy_shield_card and special_card == "holy_shield_card") or (holy_damage_card and special_card == "holy_damage_card"):
                    special_card_posy -= 50
                special_button = button.Button(special_img, special_card_posx, special_card_posy, 2.5, hover_img)
                #กดใช้ special card
                if special_button.draw(screen):
                    if (holy_pizza_card and special_card == "holy_pizza_card") or (holy_shield_card and special_card == "holy_shield_card") or (holy_damage_card and special_card == "holy_damage_card"):
                        """กดซ้ำ กลับ True เป็น False"""
                        holy_pizza_card, holy_shield_card, holy_damage_card = False, False, False
                    else:
                        holy_pizza_card, holy_shield_card, holy_damage_card = False, False, False
                        if special_card == "holy_pizza_card":
                            holy_pizza_card = True
                        elif special_card == "holy_shield_card":
                            holy_shield_card = True
                        elif special_card == "holy_damage_card":
                            holy_damage_card = True
                special_card_posx += 150

            global enemy_health, player_health, shield, atk_count
            #attack button
            if atk_button.draw(screen):
                attack = 0
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
                        my_special_cards.append(card_increase)

                    #ใช้ของ
                    if holy_pizza_card:
                        player_health.hp += 10
                        holy_pizza_card = False
                        my_special_cards.remove("holy_pizza_card")
                    elif holy_shield_card:
                        shield += 2
                        holy_shield_card = False
                        my_special_cards.remove("holy_shield_card")
                    
                    #เราตี
                    if holy_damage_card and not spam:
                        enemy_health -= attack
                        holy_damage_card = False
                        my_special_cards.remove("holy_damage_card")
                    elif holy_damage_card and spam:
                        enemy_health -= 2
                        spam = False
                        holy_damage_card = False
                        my_special_cards.remove("holy_damage_card")
                    elif spam:
                        enemy_health -= 1
                        spam = False
                    elif not spam:
                        enemy_health -= random.uniform(attack*0.2, attack)
                    
                    #หมีตี
                    if shield > 0:
                        shield -= 1
                    elif enemy_health <= 20:
                        player_health.hp -= 10
                    elif enemy_health <= 50:
                        player_health.hp -= 5
                    elif enemy_health <= 100:
                        player_health.hp -= 3
                    if enemy_health <= 0:
                        print("You Win")
                    elif player_health.hp <= 0:
                        print("You Lose")

                    word = ""

                else:
                    word = ""
                    print("please input again")

            pygame.display.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
