import numpy
import time
import turtle
import threading
import random
updateSpeed = 0.1


gamesize = 400

	
def timeKeep():
	runtime = round((time.time() - gameStartTime),2)
	return runtime
	
def updateState():
	
	global nextUpdate
	if nextUpdate < timeKeep():
		nextUpdate = timeKeep() + updateSpeed
		update = True

		return True
	update = False
	return False
	
	
def collision():
	if ball[ballPosX] > gamesize/2 or ball[ballPosX] < -gamesize / 2:
		ball[ballVelX] = -ball[ballVelX]
	if ball[ballPosY] > gamesize/2 or ball[ballPosY] < -gamesize / 2:
		ball[ballVelY] = -ball[ballVelY]
	
def ballUpdate(update):
	collision()	
	ball[ballPosX] += ball[ballVelX] * updateSpeed
	ball[ballPosY] += ball[ballVelY] * updateSpeed
	view.setx(ball[ballPosX])
	view.sety(ball[ballPosY])



view = turtle.Turtle()
view.speed(0)


ball = [0, 0, 0, 0]


ballPosX = 0
ballPosY = 1
ballVelX = 2
ballVelY = 3
global update
update = False



initialVel = 1

randomStart = random.randint(40, 100)

ball[ballVelX] = (randomStart / 100) * initialVel
ball[ballVelY] = ((initialVel ** 2) - (((randomStart / 100) * initialVel)  ** 2))**0.5


print(((ball[ballVelY]**2) + (ball[ballVelX]**2))**0.5)



gameStartTime = time.time()

nextUpdate = 2


turtle.pu()
turtle.setposition(-gamesize/2, -gamesize/2)
turtle.pd()
for i in range(4):
	turtle.forward(gamesize)
	turtle.left(90)



while True:
	#update = updateState()
	
	ballUpdate(update)

	
