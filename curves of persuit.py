import math
import turtle
import threading



size = 100
#if the square does not fit in the screen you can lower this number
stepsize = 1
#how big the step is, change this to make it  faster or to have a nicer pattern

numSides = 0
polyAngle = ((numSides-2)*180)/numSides
print(polyAngle)

draw = turtle.Turtle()
draw.pensize(0.1)
draw.speed(0)

def square(size):
	for i in range(numSides):
		draw.forward(size)
		draw.left(180 - polyAngle)
	print('Drawn...')

def centre(length):
	draw.pu()
	draw.setpos(-size/2, -size/2)
	draw.pd()
	
def calculate(size, stepsize):
	
	length = size - stepsize
	
	size = math.sqrt((length ** 2) + (stepsize ** 2) - 2 * length * stepsize * math.cos(math.radians(polyAngle)))

	angle = math.degrees(math.asin((stepsize * math.sin(math.radians(polyAngle))) / size))
	print('Calculated...')
	return size, angle
	

centre(size)

while True:
	
	squareThread = threading.Thread(target=square(size))
	squareThread.start()
	
	calcThread = threading.Thread(target=square(size))
	
	length = size - stepsize
	if length <= stepsize:
		break

	size, angle = calculate(size, stepsize)

	squareThread.join()
	draw.forward(stepsize)
	draw.left(angle)	

	

