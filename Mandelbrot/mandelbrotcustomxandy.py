import turtle
import math

startx = -2
starty = -2
screensizex = 1800
screensizey = 900
halfscreenx = screensizex / 2
halfscreeny = screensizey / 2
iteri = 0
itermax = 50
n = 0
xn = 0
yn = 0
xnplus1 = 0
ynplus1 = 0
modsq = 0
stepsizex = 2 / (screensizex / 2)
stepsizey = 2 / (screensizey / 2)
xpix = 0 - halfscreenx
ypix = 0 - halfscreeny

xc = startx
yc = starty

mand = turtle.Turtle()
mand.speed(200000)
mand.pu()
mand.goto(xpix, ypix)
mand.pd

while ypix <= halfscreeny:

    xc = startx

    xpix = 0 - halfscreenx
    while xpix <= halfscreenx:


        iteri = 0
        modsq = 0
        xn = 0
        yn = 0



        while iteri < itermax and modsq <= 4:
            
            xnplus1 = xn**2 - yn**2 + xc
            ynplus1 = (2 * xn * yn) + yc
            
            
            iteri = iteri + 1

            modsq = xnplus1**2 + ynplus1**2


            xn = xnplus1
            yn = ynplus1

        mand.goto(xpix, ypix)
        mand.pd()
        
        
        colour = 1 - (iteri / itermax)
        mand.color((colour, colour, colour))
        mand.forward(1)
        #print(xpix, ypix, xc, yc, stepsize, modsq, iteri)

        xc = xc + stepsizex

        #the round function was a test

        xpix = xpix + 1
    mand.pu()

        

    yc = yc + stepsizey
    ypix = ypix + 1
print('done')


