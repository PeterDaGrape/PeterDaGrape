import random 
import turtle


height = 300
length = height * (2/3)

pointsX = []
pointsY = []

def inRange(x, y):

	if (1.5*x - y + height < 0):
		return False
	elif (1.5*x + y -height > 0):
		return False
	elif y < 0:
		return False
	else:
		
		print(x, y)
		return True 
		
		
tri = turtle.Turtle()
tri.speed(0)
tri.penup()
tri.backward(length)
tri.sety(-200)

tri.pd()
for i in range(3): 
	tri.forward(length*2)
	tri.left(120)
	pointsX.append(tri.xcor())
	pointsY.append(tri.ycor())


tri.pu()

while True:
	
	point = [(random.randint(round(length/2 * -1), round(length / 2))), random.randint(0, round(length))]
	if inRange(point[0], point[1]):
		print(point)
		break
		


count = 0
while True:
	tri.goto(point[0], point[1])

	tri.dot(size=1)
	
	pointSelect = random.randint(0, 2)
	vertex = [pointsX[pointSelect], pointsY[pointSelect]]
	newpoint = [((point[0] + vertex[0])/2), ((point[1] + vertex[1])/2)]

	point = [newpoint[0], newpoint[1]]
	
	count += 1
	if count % 1000 == 0:
		print(count)

		

