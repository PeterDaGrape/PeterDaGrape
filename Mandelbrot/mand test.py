import turtle
import math

startx = -2
starty = -2
screensize = 100
halfscreen = screensize / 2
iteri = 0
itermax = 10
n = 0
xn = 0
yn = 0
xnplus1 = 0
ynplus1 = 0
modsq = 0
stepsize = 2 / (screensize / 2)
xpix = 0 - halfscreen
ypix = 0 - halfscreen

xc = startx
yc = starty

mand = turtle.Turtle()
mand.pu()
mand.goto(xpix, ypix)
mand.pd

while ypix <= halfscreen:



    xpix = 0 - halfscreen
    while xpix <= halfscreen:


        iteri = iteri + 1
        modsq = 0
        xn = 0
        yn = 0



        mand.goto(xpix, ypix)
        mand.pd()
        
        
        colour = 1 - (iteri / itermax)
        mand.color((colour, colour, colour))
        mand.forward(1)
        print(xpix, ypix, xc, yc, stepsize, modsq, iteri)

        xc = xc + stepsize



        xpix = xpix + 1
    mand.pu()

        

    yc = yc + stepsize
    ypix = ypix + 1
print('done')


