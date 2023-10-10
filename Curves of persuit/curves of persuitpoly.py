import math
from turtle import *
import turtle

length = 250
#if the square does not fit in the screen you can lower this number
stepsize = 40
#how big the step is, change this to make it  faster or to have a nicer pattern
cont = length / stepsize


sides = 5
print(sides)

polygon_ang = ((sides - 2) * 180) / sides
print(polygon_ang)




square = turtle.Turtle()
square.speed(6)
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
    nosteplength = length - stepsize

#for i in range(3):
    for i in range(sides):
        square.forward(length)
        square.left(180 - polygon_ang)
    square.forward(stepsize)
    #moves the pen to start drawing in the correct place

#this program uses the pythagoras theorem not trigonometry to calculate the hypotenuse
#it then uses trigonometry to calc ulate the angle that is needed to reach the desired location 
    

    length = math.sqrt((stepsize ** 2) + (nosteplength ** 2) - (2 * stepsize * nosteplength * math.cos(polygon_ang)))
    #working out the size away from the step for pythagoras to work correctly, this is the pythagoras formula


    angle = math.asin(stepsize * (math.sin(polygon_ang) / length))
    angle = math.degrees(angle)
    print('angle of attack to reach the next lines stepsize is  ', angle)
    print('the length of the hypotenuse is  ', length)
    #these commands are for the trigonometry to get the correct formula and to use degrees not radions
    square.left(angle)
    
    
    #this just makes the rest of the square
square.penup()
square.forward(2000)
#to remove the pen from the scene
