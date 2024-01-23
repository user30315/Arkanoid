import pgzrun
import os
import random
import pygame

# this line centers the game screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# setting up the game window and spirits
WIDTH, HEIGHT = 800, 600
PADDLE_HEIGHT, PADDLE_WIDTH = 20, 150
BALL_HEIGHT, BALL_WIDTH = 20, 20
pygame.display.set_caption("Arkanoid")
velocity = 5

# creating the ball and paddle and resizing them; without manipulating the images themselves; graphics is gross ;)
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

# making the ball move at an angle
ball.dx = random.choice([-velocity, velocity])
ball.dy = -velocity

# creating obstacles
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

# initializing basic game variables
lives  = 3
score =  0
game_on = True
can_move = False


def update():
    """Handle ball movement, bouncing, collisions with the obstacles, lives and score management"""
    global lives, can_move, game_on, score

    if lives <= 0 or score == (300 * bricks_in_a_column * bricks_in_a_row):
        game_on = False
        can_move = False
        paddle.center=(WIDTH/2, HEIGHT/2 + 280)
        ball.center=(WIDTH + 100, HEIGHT + 100)
        paddle.center=(WIDTH + 100, HEIGHT + 100)

    # ball movement
    if game_on and can_move:
        ball.x += ball.dx
        ball.y += ball.dy

        # bounce off the walls
        if ball.left < 0 or ball.right > WIDTH:
            ball.dx *= -1
        if ball.top < 0:
            ball.dy *= -1

        if ball.colliderect(paddle):
            if ball.dy > 0:
                ball.dy *= -1

        # collision with obstacles
        for brick in bricks:
            if ball.colliderect(brick):
                ball.dy *= -1
                bricks.remove(brick)
                score += 300

        # handling situations when the ball disappears
        if ball.bottom >= 600:
            lives -= 1
            can_move = False
            ball.center=(WIDTH/2, HEIGHT/2 + 260)
            paddle.center=(WIDTH/2, HEIGHT/2 + 280)


def on_mouse_move(pos, rel, buttons):
    """Move the paddle"""
    if can_move:
        paddle.x = pos[0] + PADDLE_WIDTH


def on_mouse_down():
    """Click to start the game"""
    global can_move
    can_move = True


def draw():
    """Main game loop; draws all the actors and manages the game."""
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
