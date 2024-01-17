import pgzrun
import os
import random
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH, HEIGHT = 800, 600
PADDLE_HEIGHT, PADDLE_WIDTH = 20, 150
BALL_HEIGHT, BALL_WIDTH = 20, 20
pygame.display.set_caption("Arkanoid")

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
ball.dx = random.choice([-2, 2])
ball.dy = -2

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

velocity = 2
game_on = True
can_move = False

def update():

    if game_on and can_move:
        ball.x += ball.dx
        ball.y += ball.dy

        if ball.left < 0 or ball.right > WIDTH:
            ball.dx *= -1
        if ball.top < 0:
            ball.dy *= -1

        if ball.colliderect(paddle):
            ball.dy *= -1

        for brick in bricks:
            if ball.colliderect(brick):
                ball.dy *= -1
                bricks.remove(brick)


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

pgzrun.go()
