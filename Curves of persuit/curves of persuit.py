import math
from turtle import *
import turtle

length = 700
#if the square does not fit in the screen you can lower this number
stepsize = 5
#how big the step is, change this to make it  faster or to have a nicer pattern

cont = length / stepsize

square = turtle.Turtle()
square.speed(2000)
#setting up the draw function and variables
square.penup()
square.left(180)
square.forward(length / 2)
square.left(90)
square.forward(length / 2)
square.left(90)
square.pendown()
#putting the pen so the centre of the square is in the middle



for i in range(int(cont)):
    for i in range(4):
        square.forward(length)
        square.left(90)
    square.forward(stepsize)
    #moves the pen to start drawing in the correct place
    length = math.sqrt(((length - stepsize) ** 2) + (stepsize ** 2))
    #working out the size away from the step for pythagoras to work correctly, this is the pythagoras formula
    angle = math.asin(stepsize / length)
    angle = math.degrees(angle)
    #these commands are for the trigonometry to get the correct formula and to use degrees not radions
    square.left(angle)
    
    
    #this just makes the rest of the square
square.penup()
square.forward(2000)
#to remove the pen from the scene
