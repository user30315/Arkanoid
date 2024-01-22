import pgzrun
import os
import random
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH, HEIGHT = 800, 600
PADDLE_HEIGHT, PADDLE_WIDTH = 20, 150
BALL_HEIGHT, BALL_WIDTH = 20, 20
pygame.display.set_caption("Arkanoid")
velocity = 5

paddle = Actor("paddle")

paddle.width = PADDLE_WIDTH
paddle.height = PADDLE_HEIGHT
paddle._surf = pygame.transform.scale(paddle._surf, (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle.center=(WIDTH/2, HEIGHT/2 + 280)

ball = Actor("ball")
ball.width = BALL_WIDTH
ball.height = BALL_HEIGHT
ball._surf = pygame.transform.scale(ball._surf, (BALL_WIDTH, BALL_HEIGHT))
ball.center=(WIDTH/2, HEIGHT/2 + 260)
ball.dx = random.choice([-velocity, velocity])
ball.dy = -velocity

BRICK_WIDTH, BRICK_HEIGHT = 80, 20
bricks_in_a_row = 9
bricks_in_a_column = 4
brick_images = ["blue-brick", "green-brick", "red-brick", "orange-brick", "yellow-brick", "gray-brick"]
bricks = []
for i in range(bricks_in_a_column):
    for j in range(bricks_in_a_row):
        brick = Actor(random.choice(brick_images))
        brick.width, brick.height = BRICK_WIDTH, BRICK_HEIGHT
        brick._surf = pygame.transform.scale(brick._surf, (BRICK_WIDTH, BRICK_HEIGHT))
        brick.x = 240 + BRICK_WIDTH * j
        brick.y = 400 + BRICK_HEIGHT * i
        bricks.append(brick)

lives  = 3
score =  0
game_on = True
can_move = False

def update():
    global lives
    global can_move
    global game_on
    global score

    if lives <= 0 or score == (300 * bricks_in_a_column * bricks_in_a_row):
        game_on = False
        can_move = False
        paddle.center=(WIDTH/2, HEIGHT/2 + 280)
        ball.center=(WIDTH + 100, HEIGHT + 100)
        paddle.center=(WIDTH + 100, HEIGHT + 100)

    if game_on and can_move:
        ball.x += ball.dx
        ball.y += ball.dy

        if ball.left < 0 or ball.right > WIDTH:
            ball.dx *= -1
        if ball.top < 0:
            ball.dy *= -1

        if ball.colliderect(paddle):
            reflection_angle = (ball.x - paddle.x) / paddle.width
            ball.dx = velocity * reflection_angle
            ball.dy *= -1

        for brick in bricks:
            if ball.colliderect(brick):
                ball.dy *= -1
                bricks.remove(brick)
                score += 300

        if ball.bottom >= 600:
            lives -= 1
            can_move = False
            ball.center=(WIDTH/2, HEIGHT/2 + 260)
            paddle.center=(WIDTH/2, HEIGHT/2 + 280)


def on_mouse_move(pos, rel, buttons):
    if can_move:
        paddle.x = pos[0] + PADDLE_WIDTH
        # actor.y = pos[1]


def on_mouse_down():
    global can_move
    can_move = True

def draw():
    screen.fill((0, 0, 0))
    ball.draw()
    paddle.draw()
    for brick in bricks:
        brick.draw()
    screen.draw.text(f"Lives: {lives}", (WIDTH/2 - 80, HEIGHT/2 - 250), fontsize=60, color="red", gcolor="purple")
    screen.draw.text(f"Score: {score}", (WIDTH/2 - 85, HEIGHT/2 - 200), fontsize=60, color="red", gcolor="purple")
    if lives == 0:
        screen.fill((0, 0, 0))
        ball.draw()
        paddle.draw()
        screen.draw.text("GAME OVER!", (40, HEIGHT/2 - 50), fontsize=160, color="yellow", gcolor="red")
    if score == (300 * bricks_in_a_column * bricks_in_a_row):
        screen.draw.text("GAME WON!", (60, HEIGHT/2 - 50), fontsize=160, color="yellow", gcolor="blue")

pgzrun.go()
