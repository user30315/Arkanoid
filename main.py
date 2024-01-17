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
paddle._surf = pygame.transform.scale(paddle._surf, (150, 20))
paddle.center=(WIDTH/2 + 150, HEIGHT/2 + 280)

ball = Actor("ball")
ball.width = BALL_WIDTH
ball.height = BALL_HEIGHT
ball._surf = pygame.transform.scale(ball._surf, (20, 20))
ball.center=(WIDTH/2, HEIGHT/2 + 260)
ball.dx = random.choice([-2, 2])
ball.dy = -2

# brick_count = 5
# brick_images = ["blueBrick", "greenBrick", "redBrick", "orangeBrick", "yellowBrick"]
# bricks = [Actor(random.choice(brick_images)) for actor in range(brick_count)]

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
        
        # if (ball.x - BALL_WIDTH - paddle.x - PADDLE_WIDTH) <= 50 and (ball.y - BALL_HEIGHT - paddle.y - PADDLE_HEIGHT) <= 50:
        #     print("collision")
        #     ball.dy *= -1
        if ball.colliderect(paddle):
            ball.dy *= -1


def on_mouse_move(pos, rel, buttons):
    if can_move:
        paddle.x = pos[0] + PADDLE_WIDTH
        # actor.y = pos[1]


def on_mouse_down():
    global can_move
    can_move = True
    print(f"Ball x   {ball.x - BALL_WIDTH}")
    print(f"Ball y   {ball.y - BALL_HEIGHT}")
    print(f"paddle x   {paddle.x - PADDLE_WIDTH}")
    print(f"paddle y   {paddle.y - PADDLE_HEIGHT}")

def draw():
    screen.fill((0, 0, 0))
    ball.draw()
    paddle.draw()

pgzrun.go()
