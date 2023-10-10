
import turtle
import math


startx = -2
starty = -1.25
stopx = 0.75
stopy = 1.25

screensizex = 1000
#the higher this number the larger the image will be but it will run a lot slower
screensizey = int(screensizex * (stopy - starty) / (stopx - startx))
print(screensizex, screensizey)
halfscreenx = screensizex / 2
halfscreeny = screensizey / 2
iteri = 0
itermax = 100
xn = 0
yn = 0
xnplus1 = 0
ynplus1 = 0
modsq = 0
stepsizex = (stopx - startx) / screensizex
stepsizey = (stopy - starty) / screensizey
xpix = 0 - halfscreenx
ypix = 0 - halfscreeny

xc = startx
yc = starty

mand = turtle.Turtle()
mand.speed(0)
mand.pu()
mand.goto(xpix, ypix)
mand.pd

turtle.tracer(0, 0)



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
        
        mand.speed(0)
        colour = 1 - (iteri / itermax)
        mand.color((colour, colour, colour))
        mand.forward(1)
        #print(xpix, ypix, xc, yc, stepsizex, stepsizey, modsq, iteri)

        xc = round((xc + stepsizex), 5)



        xpix = xpix + 1
    mand.pu()

        

    yc = round((yc + stepsizey), 5)
    ypix = ypix + 1

turtle.update()
print('done')


