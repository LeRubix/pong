import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 20
FPS = 60
FONT_SIZE = 50

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self, y):
        self.rect.y = y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Ball class
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = 7
        self.speed_y = 7

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

        # Ball collision with paddles
        if self.rect.colliderect(player_paddle.rect) or self.rect.colliderect(opponent_paddle.rect):
            self.speed_x = -self.speed_x

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.speed_x *= -1

# Initialize paddles and ball
player_paddle = Paddle(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
opponent_paddle = Paddle(10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)

# Scores
player_score = 0
opponent_score = 0

# Clock
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mouse control for player paddle
    mouse_y = pygame.mouse.get_pos()[1]
    player_paddle.move(mouse_y - PADDLE_HEIGHT // 2)

    # AI control for opponent paddle
    if opponent_paddle.rect.centery < ball.rect.centery:
        opponent_paddle.rect.y += 5
    if opponent_paddle.rect.centery > ball.rect.centery:
        opponent_paddle.rect.y -= 5

    # Move ball
    ball.move()

    # Check for scoring
    if ball.rect.left <= 0:
        player_score += 1
        ball.reset()
    if ball.rect.right >= SCREEN_WIDTH:
        opponent_score += 1
        ball.reset()

    # Draw everything
    screen.fill(BLACK)
    player_paddle.draw()
    opponent_paddle.draw()
    ball.draw()

    # Draw scores
    player_text = font.render(f"{player_score}", True, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH - 100, 50))
    opponent_text = font.render(f"{opponent_score}", True, WHITE)
    screen.blit(opponent_text, (50, 50))

    # Update display
    pygame.display.flip()

    # Frame rate
    clock.tick(FPS)
