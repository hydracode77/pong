import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
background = pygame.image.load("graphics/background.jpg").convert()
pong_screen = pygame.image.load("graphics/pong screen.png").convert_alpha()
game_active = False


class Sound:
    wall = pygame.mixer.Sound("sounds/wall_sound.mp3")
    score = pygame.mixer.Sound("sounds/score_sound.mp3")
    hit = pygame.mixer.Sound("sounds/hit_sound.mp3")
    wall.set_volume(0.2)
    score.set_volume(0.08)
    hit.set_volume(0.2)


class Player:
    surface = pygame.image.load("graphics/player.png").convert_alpha()
    right_y = 1080
    left_y = 1080
    rect_right = surface.get_rect(bottomright=(1889, right_y))
    rect_left = surface.get_rect(bottomright=(57, left_y))
    bot_active = False
    bot_randomness = randint(-50, 100)  # damit Bot fehlerhaft ist, soll nicht genau beim ball sein
    time_to_random_bot = 0


class Ball:
    surface = pygame.image.load("graphics/ball.png").convert_alpha()
    x = 970
    y = 550
    rect = surface.get_rect(bottomright=(x, y))
    x_speed = 10
    y_speed = 13


class Score:
    zero = pygame.image.load("graphics/number/0.png").convert_alpha()
    one = pygame.image.load("graphics/number/1.png").convert_alpha()
    two = pygame.image.load("graphics/number/2.png").convert_alpha()
    three = pygame.image.load("graphics/number/3.png").convert_alpha()
    four = pygame.image.load("graphics/number/4.png").convert_alpha()
    five = pygame.image.load("graphics/number/5.png").convert_alpha()
    six = pygame.image.load("graphics/number/6.png").convert_alpha()
    seven = pygame.image.load("graphics/number/7.png").convert_alpha()
    eight = pygame.image.load("graphics/number/8.png").convert_alpha()
    nine = pygame.image.load("graphics/number/9.png").convert_alpha()
    liste = [zero, one, two, three, four, five, six, seven, eight, nine]
    right_score = 0
    left_score = 0
    current_right = liste[right_score]
    current_left = liste[left_score]
    rect_right = one.get_rect(bottomright=(1189, 178))
    rect_left = one.get_rect(bottomright=(786, 178))
    right_lost = False
    right_lost_surf = pygame.image.load("graphics/right_lost.png").convert_alpha()
    left_lost = False
    left_lost_surf = pygame.image.load("graphics/left_lost.png").convert_alpha()
    blit_PONG = True
    bot_button = pygame.image.load("graphics/b.png").convert_alpha()
    bot_rect = bot_button.get_rect(topleft=(1078, 452))
    player_button = pygame.image.load("graphics/p.png").convert_alpha()
    player_rect = player_button.get_rect(topleft=(694, 452))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    if game_active:
        screen.blit(background, (0, 0))

        # Player movement
        Player.rect_left = Player.surface.get_rect(bottomright=(57, Player.left_y))
        Player.rect_right = Player.surface.get_rect(bottomright=(1889, Player.right_y))
        pressed = pygame.key.get_pressed()

        # Buttons
        if pressed[pygame.K_w]:
            Player.left_y -= 15
            if Player.left_y <= 135:
                Player.left_y = 135

        if pressed[pygame.K_s]:
            Player.left_y += 15
            if Player.left_y >= 1080:
                Player.left_y = 1080

        if not Player.bot_active:
            if pressed[pygame.K_UP]:
                Player.right_y -= 15
                if Player.right_y <= 135:
                    Player.right_y = 135

            if pressed[pygame.K_DOWN]:
                Player.right_y += 15
                if Player.right_y >= 1080:
                    Player.right_y = 1080
        else:
            Player.right_y = Ball.y + Player.bot_randomness
            if Player.right_y <= 135:
                Player.right_y = 135
            if Player.right_y >= 1080:
                Player.right_y = 1080

        # Ball Movement
        Ball.x += Ball.x_speed
        Ball.y += Ball.y_speed
        Ball.rect = Ball.surface.get_rect(bottomright=(Ball.x, Ball.y))

        # oben & unten abprallen
        if Ball.y < 0 or Ball.y > 1080:
            Ball.y_speed *= -1
            Sound.wall.play()

        # am player abprallen
        if Ball.rect.colliderect(Player.rect_right) or Ball.rect.colliderect(Player.rect_left):
            Ball.x_speed *= -1
            Ball.y_speed = randint(5, 15)
            Sound.hit.play()

        # Links scored
        if Ball.x >= 2000:
            Score.left_score += 1
            Sound.score.play()
            Player.bot_randomness = randint(-50, 100)  # bei jedem Score lil Pos änderung vom Bot
            if Score.left_score == 9:
                game_active = False
                Score.right_lost = True
            Score.current_left = Score.liste[Score.left_score]
            Ball.x = 1620
            Ball.x_speed *= -1

        # Rechts scored
        if Ball.x <= -80:
            Score.right_score += 1
            Sound.score.play()
            Player.bot_randomness = randint(-50, 100)
            if Score.right_score == 9:
                game_active = False
                Score.left_lost = True
            Score.current_right = Score.liste[Score.right_score]
            Ball.x = 300
            Ball.x_speed *= -1

        screen.blit(Score.current_right, Score.rect_right)
        screen.blit(Score.current_left, Score.rect_left)
        screen.blit(Player.surface, Player.rect_left)
        screen.blit(Player.surface, Player.rect_right)
        screen.blit(Ball.surface, Ball.rect)

    else:
        pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_state = pygame.mouse.get_pressed()

        if Score.left_lost:
            screen.blit(Score.left_lost_surf, (0, 0))

        elif Score.right_lost:
            screen.blit(Score.right_lost_surf, (0, 0))

        elif Score.blit_PONG:
            screen.blit(background, (0, 0))
            screen.blit(pong_screen, (0, 0))
            screen.blit(Score.current_right, Score.rect_right)
            screen.blit(Score.current_left, Score.rect_left)
            screen.blit(Player.surface, Player.rect_left)
            screen.blit(Player.surface, Player.rect_right)
            if pressed[pygame.K_RETURN] or pressed[pygame.K_SPACE]:
                Score.blit_PONG = False

        else:
            screen.blit(background, (0, 0))
            screen.blit(Score.current_right, Score.rect_right)
            screen.blit(Score.current_left, Score.rect_left)
            screen.blit(Player.surface, Player.rect_left)
            screen.blit(Player.surface, Player.rect_right)
            screen.blit(Score.bot_button, Score.bot_rect)
            screen.blit(Score.player_button, Score.player_rect)

            if mouse_state[0]:
                if Score.bot_rect.collidepoint(mouse_pos):
                    Player.bot_active = True
                    game_active = True
                    Score.left_score = 0
                    Score.right_score = 0
                    Player.right_y = 1080
                    Player.left_y = 1080
                    Ball.x = 970
                    Ball.y = 550
                    Score.left_lost = False
                    Score.right_lost = False
                elif Score.player_rect.collidepoint(mouse_pos):
                    Player.bot_active = False
                    game_active = True
                    Score.left_score = 0
                    Score.right_score = 0
                    Player.right_y = 1080
                    Player.left_y = 1080
                    Ball.x = 970
                    Ball.y = 550
                    Score.left_lost = False
                    Score.right_lost = False

    pygame.display.update()
    clock.tick(60)
