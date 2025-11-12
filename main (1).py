import pygame, sys
from button import Button
import sys 
import random 

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Mäng")

BG = pygame.image.load("Jõuluprojekt/assets/taust1.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Jõuluprojekt/assets/font.ttf", size)

def play():
    clock = pygame.time.Clock()
    font = get_font(35)

    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    speed = 15

    food_pos = [random.randrange(1, 128)*10, random.randrange(1, 72)*10]
    food_spawn = True
    score = 0

    def game_over():
        go_font = get_font(60)
        go_surf = go_font.render("Game Over!", True, "red")
        go_rect = go_surf.get_rect(center=(640, 360))
        SCREEN.blit(go_surf, go_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        main_menu()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to

        if direction == 'UP':
            snake_pos[1] -= 10
        elif direction == 'DOWN':
            snake_pos[1] += 10
        elif direction == 'LEFT':
            snake_pos[0] -= 10
        elif direction == 'RIGHT':
            snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, 128)*10, random.randrange(1, 72)*10]
        food_spawn = True

        SCREEN.fill("black")

        for block in snake_body:
            pygame.draw.rect(SCREEN, "green", pygame.Rect(block[0], block[1], 10, 10))

        pygame.draw.rect(SCREEN, "red", pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if (snake_pos[0] < 0 or snake_pos[0] > 1270 or
            snake_pos[1] < 0 or snake_pos[1] > 710):
            game_over()

        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()

        score_text = font.render(f"Skoor: {score}", True, "white")
        SCREEN.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(speed)
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("purple")

        OPTIONS_TEXT = get_font(45).render("Tõesti lootsid settingute olemasolule?", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Menüü", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Jõuluprojekt/assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Jõuluprojekt/assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Jõuluprojekt/assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Red")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()