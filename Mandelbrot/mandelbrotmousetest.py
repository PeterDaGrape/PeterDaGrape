
import turtle
import math
import time


x = 0
y = 0
startx = -2
stopx = 2
starty = -2
stopy = 2
zoom = 1

screensizex = 250



screensizey = screensizex

print(screensizex, screensizey)
halfscreenx = screensizex / 2
halfscreeny = screensizey / 2
iteri = 0
itermax = 50
xn = 0
yn = 0
xnplus1 = 0
ynplus1 = 0
modsq = 0

mand = turtle.Turtle()
mand.speed(0)
turtle.tracer(0, 0)
while True:
    stepsizex = (stopx - startx) / screensizex
    stepsizey = (stopy - starty) / screensizey
    xpix = 0 - halfscreenx
    ypix = 0 - halfscreeny

    xc = startx
    yc = starty



    mand.pu()
    mand.goto(xpix, ypix)
    mand.pd()

    
    yc = starty
    
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


    print('done')
    turtle.update()


    centrex = float(input('zoom coordinate x '))
    centrey = float(input('zoom coordinate y '))
    zoom = float(input('zoom multiplier '))
    mandwidth = 4 / zoom
    halfmandwid = mandwidth / 2
    startx = centrex - halfmandwid
    stopx = centrex + halfmandwid
    starty = centrey - halfmandwid
    stopy = centrey + halfmandwid
    



    


