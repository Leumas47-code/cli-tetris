import pygame
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
CLOCK = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Fonts
FONT = pygame.font.Font(None, 36)

# Game objects
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Initialize paddles and ball
player = pygame.Rect(WIDTH - 20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Score
player_score = 0
opponent_score = 0

# Game state
game_started = False
players = 1  # default mode


def draw_button(text, rect, selected=False):
    pygame.draw.rect(SCREEN, GREEN if selected else GRAY, rect)
    label = FONT.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    SCREEN.blit(label, label_rect)


def show_menu():
    SCREEN.fill(BLACK)
    title = FONT.render("Select Mode and Start", True, WHITE)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

    draw_button("1 Player", one_btn, players == 1)
    draw_button("2 Players", two_btn, players == 2)
    draw_button("Start", start_btn)

    pygame.display.flip()

# Menu buttons
one_btn = pygame.Rect(WIDTH // 2 - 110, 150, 100, 50)
two_btn = pygame.Rect(WIDTH // 2 + 10, 150, 100, 50)
start_btn = pygame.Rect(WIDTH // 2 - 50, 250, 100, 50)


def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    BALL_SPEED_X *= -1
    BALL_SPEED_Y *= -1


# Game loop
while True:
    if not game_started:
        show_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if one_btn.collidepoint(event.pos):
                    players = 1
                elif two_btn.collidepoint(event.pos):
                    players = 2
                elif start_btn.collidepoint(event.pos):
                    game_started = True
                    player_score = 0
                    opponent_score = 0
                    reset_ball()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += PADDLE_SPEED

        if players == 2:
            if keys[pygame.K_w] and opponent.top > 0:
                opponent.y -= PADDLE_SPEED
            if keys[pygame.K_s] and opponent.bottom < HEIGHT:
                opponent.y += PADDLE_SPEED
        else:
            if opponent.centery < ball.centery:
                opponent.y += PADDLE_SPEED
            if opponent.centery > ball.centery:
                opponent.y -= PADDLE_SPEED

        opponent.clamp_ip(SCREEN.get_rect())
        player.clamp_ip(SCREEN.get_rect())

        # Ball movement
        ball.x += BALL_SPEED_X
        ball.y += BALL_SPEED_Y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            BALL_SPEED_Y *= -1

        if ball.colliderect(player) or ball.colliderect(opponent):
            BALL_SPEED_X *= -1

        if ball.left <= 0:
            player_score += 1
            reset_ball()
        if ball.right >= WIDTH:
            opponent_score += 1
            reset_ball()

        # Draw
        SCREEN.fill(BLACK)
        pygame.draw.rect(SCREEN, WHITE, player)
        pygame.draw.rect(SCREEN, WHITE, opponent)
        pygame.draw.ellipse(SCREEN, WHITE, ball)
        pygame.draw.aaline(SCREEN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Score
        player_text = FONT.render(str(player_score), True, WHITE)
        opponent_text = FONT.render(str(opponent_score), True, WHITE)
        SCREEN.blit(player_text, (WIDTH // 2 + 20, 20))
        SCREEN.blit(opponent_text, (WIDTH // 2 - 40, 20))

        pygame.display.flip()
        CLOCK.tick(60)
