# Example file showing a circle moving on screen
import pygame
import random


def simpleAI(paddleY, targetY):
	if targetY > paddleY:
		paddleY += simpleDifficulty

	else:
		paddleY -= simpleDifficulty

	return paddleY 

def collision(ball, paddle_rect):
    ball_rect = pygame.Rect(ball.x - ballRad, ball.y - ballRad, ballRad*2, ballRad*2)
    if ball_rect.colliderect(paddle_rect):
        # Collision detected
        return True
    else:
        # No collision detected
        return False

resolution = (1280, 720)
accelerationDecay = 0.9995
global simpleDifficulty


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

dt = 0

global paddle1Y

paddleHeight = 90


ballRad = 10
ball = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


global ballPosY

global ballVec

while True:
	acceleration = 0.001
	simpleDifficulty = 4
	
	paddle1Y = resolution[1] / 2
	paddle2Y = resolution[1] / 2

	gameOver = False

	initialVel = 4

	randomStart = random.randint(40, 100)
	ballPosX, ballPosY = resolution[0] / 2, resolution[1] / 2
	ballVelX = (randomStart / 100) * initialVel
	ballVelY = ((initialVel ** 2) - (((randomStart / 100) * initialVel)  ** 2))**0.5

	while gameOver != True:

		# pygame.QUIT event means the user clicked X to close your window
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver = True

		# fill the screen with a color to wipe away anything from last frame

		paddle1 = pygame.Rect(0.075*resolution[0], paddle1Y - paddleHeight/2, 10, paddleHeight)
		paddle2 = pygame.Rect(0.925*resolution[0], paddle2Y - paddleHeight/2, 10, paddleHeight)

		screen.fill("white")

		pygame.draw.circle(screen, "red", ball, ballRad)
		pygame.draw.rect(screen, 'black', paddle1)
		pygame.draw.rect(screen, 'black', paddle2)


		
		if collision(ball, paddle1):
			ballVelX = -ballVelX
		elif collision(ball, paddle2):
			ballVelX = -ballVelX
		if ballPosY < 0 or ballPosY > resolution[1]:
			ballVelY = -ballVelY
		if ballPosX < 0:
			winner = 1
			gameOver = True
			print('Player 2 wins')
		elif ballPosX > resolution[0]:
			gameOver = True
			winner = 2
			print('Player 1 wins')

		
		

		ballPosX += ballVelX
		ballPosY += ballVelY
		paddle1Y = simpleAI(paddle1Y, ballPosY)
		paddle2Y = ballPosY



		ball.xy = ballPosX, ballPosY

		
			

		




		# flip() the display to put your work on screen
		pygame.display.flip()

		# limits FPS to 60
		# dt is delta time in seconds since last frame, used for framerate-
		# independent physics.
		dt = clock.tick(60) / 1000

		ballVelX = ballVelX + acceleration * ballVelX
		ballVelY = ballVelY + acceleration * ballVelY
		acceleration *= accelerationDecay

	

		

pygame.quit()