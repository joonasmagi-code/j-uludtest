import pygame
from button import Button
import sys
import random

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Mäng")

BG = pygame.image.load("Jõuluprojekt/assets/taust1.jpg")

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Jõuluprojekt/assets/font.ttf", size)

def play():
    clock = pygame.time.Clock()
    font = get_font(35)

    # --- Taustapilt ---
    try:
        teepilt = pygame.image.load("Jõuluprojekt/assets/teepilt.png")
        teepilt = pygame.transform.scale(teepilt, (SCREEN.get_width(), SCREEN.get_height()))
    except Exception:
        teepilt = None

    # --- Autode pildid ---
    mangijaauto = pygame.image.load("Jõuluprojekt/assets/mangijaauto.png")
    mangijaauto = pygame.transform.scale(mangijaauto, (80, 120))

    takistusauto = pygame.image.load("Jõuluprojekt/assets/takistusauto.png")
    takistusauto = pygame.transform.scale(takistusauto, (80, 120))

    car_width, car_height = 80, 120
    car_lane = 1
    car_y = 550
    lane_width = SCREEN.get_width() // 3

    def lane_center(lane_index):
        return lane_width * lane_index + lane_width // 2

    car_rect = pygame.Rect(lane_center(car_lane) - car_width // 2,
                           car_y, car_width, car_height)

    obstacles = []
    obstacle_timer = 0
    obstacle_interval = 1500
    score = 0
    start_ticks = pygame.time.get_ticks()
    game_over_flag = False

    # --- Algne kiirus ---
    obstacle_speed = 8

    def game_over():
        nonlocal game_over_flag, score
        game_over_flag = True
        go_font = get_font(60)
        score_font = get_font(40)

        go_surf = go_font.render("Game Over!", True, "red")
        go_rect = go_surf.get_rect(center=(640, 300))
        SCREEN.blit(go_surf, go_rect)

        score_surf = score_font.render(f"Sinu skoor: {score}", True, "white")
        score_rect = score_surf.get_rect(center=(640, 380))
        SCREEN.blit(score_surf, score_rect)

        pygame.display.flip()
        pygame.time.wait(3000)
        main_menu()

    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not game_over_flag:
                if event.key == pygame.K_LEFT and car_lane > 0:
                    car_lane -= 1
                elif event.key == pygame.K_RIGHT and car_lane < 2:
                    car_lane += 1

        if not game_over_flag:
            car_rect.x = lane_center(car_lane) - car_width // 2

            obstacle_timer += dt
            if obstacle_timer >= obstacle_interval:
                obstacle_timer = 0
                lane = random.randint(0, 2)
                obs_rect = pygame.Rect(lane_center(lane) - car_width // 2,
                                       -120, car_width, car_height)
                obstacles.append(obs_rect)

            # --- Kiiruse dünaamika: iga 10 punkti järel kiireneb ---
            obstacle_speed = 8 + (score // 10) * 2

            for obs in obstacles:
                obs.y += obstacle_speed
            obstacles = [o for o in obstacles if o.y < 800]

            for obs in obstacles:
                if car_rect.colliderect(obs):
                    game_over()

            score = (pygame.time.get_ticks() - start_ticks) // 1000

        # --- Joonistamine ---
        if teepilt:
            SCREEN.blit(teepilt, (0, 0))
        else:
            SCREEN.fill((50, 50, 50))

        # Tume kollased katkestatud liikuvad teejooned
        dash_length = 80
        dash_gap = 20
        line_width = 8
        line_offset = (pygame.time.get_ticks() // 10) % (dash_length + dash_gap)

        for i in range(1, 3):  # kahe vahejoone jaoks
            x = lane_width * i
            for y in range(-dash_length, SCREEN.get_height(), dash_length + dash_gap):
                pygame.draw.line(SCREEN, (200, 200, 0), (x, y + line_offset), (x, y + dash_length + line_offset), line_width)

        # Mängija auto
        SCREEN.blit(mangijaauto, car_rect)

        # Takistusautod
        for obs in obstacles:
            SCREEN.blit(takistusauto, obs)

        score_text = font.render(f"Skoor: {score}", True, "white")
        SCREEN.blit(score_text, (10, 10))

        pygame.display.update()

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
