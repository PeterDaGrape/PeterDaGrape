import math
from turtle import *
import turtle

length = 100
#if the square does not fit in the screen you can lower this number
stepsize = 20
#how big the step is, change this to make it  faster or to have a nicer pattern
angles = []
numsides = 8
#how many sides the shape has
primangle = 360 / numsides

lengths = []
cont = length / stepsize
lengthcalc = length
lengthcalc1 = length
#setting all the variables
secside = 180 - 360 / numsides







for i in range(int(cont)):




    lengthcalc = math.sqrt(((lengthcalc - stepsize) ** 2) + (stepsize ** 2))


    angle = math.asin(stepsize / lengthcalc)
    angle = math.degrees(angle)

        

    l1 = length * math.cos(angle)

    lmid = length * math.sin(angle)

    l2 = lmid * math.tan(180 - (360 / numsides))

    lengthcalc = l1 + l2




    angles.append(angle)
    lengths.append(lengthcalc)

    
    
square = turtle.Turtle()
square.speed(2000)
square.pensize(0.25)
#setting up the draw function
square.penup()
square.left(180)
square.forward(length / 2)
square.left(90)
square.forward(length / 2)
square.left(90)
square.pendown()
#putting the pen so the centre of the square is in the middle
for i in range(numsides):
    square.forward(length)
    square.left(primangle)

#draws the basic start square


for i in range(int(cont)):
    square.forward(stepsize)
    #moves the pen to start drawing in the correct place

    square.left(angles.pop(0))
    square_size = lengths.pop(0)
    for i in range(numsides):
        square.forward(square_size)
        square.left(primangle)
    
    #this just makes the rest of the square
square.penup()
square.forward(2000)
#to remove the pen from the scene

