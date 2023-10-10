import math
from turtle import *
import turtle

length = 200
#if the square does not fit in the screen you can lower this number
stepsize = 20
#how big the step is, change this to make it  faster or to have a nicer pattern
angles = []
numsides = 4
#how many sides the shape has
primangle = 360 / numsides

lengths = []
cont = length / stepsize
#length / stepsize
lengthcalc = length
#setting all the variables

for i in range(int(cont)):


    angle = math.asin(stepsize / lengthcalc)
    angle = math.degrees(angle)


    clen = lengthcalc - stepsize
    Bangle = primangle
    Cangle = 180 - primangle - angle
     
    print('angle of C', Cangle)
    
    #these commands are for the trigonometry to get the correct formula and to use degrees not radions
    angles.append(angle)
    lengthcalc = math.sqrt(((lengthcalc - stepsize) ** 2) + (stepsize ** 2))

    #lengthcalc = (clen * math.sin(Bangle)) / math.sin(Cangle)


    print('b is', lengthcalc)
    print('B is', primangle)

    print('length of c', lengthcalc-stepsize)

    #working out the size away from the step for pythagoras to work correctly, this is the pythagoras formula
    lengths.append(lengthcalc)


square = turtle.Turtle()
square.speed(0)
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
turtle.tracer(0, 0)
for i in range(numsides):
    square.forward(length)
    square.left(primangle)

#draws the basic start square


for i in range(int(cont)):
    square.forward(stepsize)
    #moves the pen to start drawing in the correct place

    square.left(angles.pop(0))
    square_size = lengths.pop(0)
    for i in range(4):
        square.forward(square_size)
        square.left(primangle)
    
    #this just makes the rest of the square
square.penup()
square.forward(2000)
#to remove the pen from the scene
turtle.update

