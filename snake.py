import pygame
import random

pygame.init()

def draw_grid():
    for x in range(0, WIDTH, 20):
        pygame.draw.line(WIN, (0, 0, 0), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 20):
        pygame.draw.line(WIN, (0, 0, 0), (0, y), (WIDTH, y))

def draw_char():
    global head, food, food_x, food_y, snake_body

    head = pygame.draw.rect(WIN, (0, 0, 255), (snake_body[0][0], snake_body[0][1], snake_size, snake_size))

    # Draw snake body
    for segment in snake_body[1:]:
        pygame.draw.rect(WIN, (0, 0, 255), (segment[0], segment[1], snake_size, snake_size))

    food = pygame.draw.rect(WIN, (255, 0, 0), (food_x, food_y, 20, 20))

def movement():
    global snake_body, current_score, high_score

    if direction == "up":
        new_head = (snake_body[0][0], snake_body[0][1] - 20)

    elif direction == "left":
        new_head = (snake_body[0][0] - 20, snake_body[0][1])

    elif direction == "down":
        new_head = (snake_body[0][0], snake_body[0][1] + 20)

    elif direction == "right":
        new_head = (snake_body[0][0] + 20, snake_body[0][1])

    # Check if new position collides with snake's body
    if new_head in snake_body[1:]:
        game_over()

    # Check if new position is out of bounds
    if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
        # If out of bounds, wrap around to the opposite side
        new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)

    snake_body.insert(0, new_head)
    if len(snake_body) > snake_length:
        snake_body.pop()

    if new_head == (food_x, food_y):
        current_score += 1
        if current_score > high_score:
            high_score = current_score
            set_highscore()

def food_collision():
    global food_x, food_y, snake_length

    if snake_body[0][0] == food_x and snake_body[0][1] == food_y:
        food_x = random.randint(0, (WIDTH - 20) // 20) * 20
        food_y = random.randint(0, (HEIGHT - 20) // 20) * 20
        snake_length += 1

def game_over():
    global snake_body, snake_length, direction, current_score

    snake_body = [(WIDTH // 2, HEIGHT // 2)]
    snake_length = 1
    direction = "right"
    current_score = 0

def set_highscore():
    try:
        file = open("highscore.txt", "w")
        file.write(str(high_score))
        file.close

    except:
        pass


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

snake_body = [(WIDTH // 2, HEIGHT // 2)]
snake_size = 20
snake_length = 1
food_x = random.randint(0, (WIDTH - 20) // 20) * 20
food_y = random.randint(0, (HEIGHT - 20) // 20) * 20
direction = "right"

current_score = 0
try:
    file = open("highscore.txt", "r")
    high_score = int(file.read())
    file.close()

except:
    high_score = 0

font = pygame.font.SysFont("arial", 36)

running = True
while running:
    clock.tick(10)
    WIN.fill((0, 255, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                direction = "up"

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                direction = "left"

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                direction = "down"

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                direction = "right"

    draw_char()
    draw_grid()
    movement()
    food_collision()
    draw_text(f"Current Score: {current_score}", font, (255, 255, 255), WIN, WIDTH // 2, 30)
    draw_text(f"High Score: {high_score}", font, (255, 255, 255), WIN, WIDTH // 2, 60)
    pygame.display.update()

pygame.quit()
