# Example showing how functions, that accept tuples of rgb values,
# simplify working with gradients

import time
from neopixel import Neopixel
import _thread


numpix = 294
strip = Neopixel(numpix, 0, 18, "GRB")
# strip = Neopixel(numpsix, 0, 0, "GRBW")

red = (255, 0, 0)
orange = (255, 50, 0)
yellow = (255, 100, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
indigo = (100, 0, 90)
violet = (200, 0, 100)
colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

# same colors as normaln rgb, just 0 added at the end
colors_rgbw = [color+tuple([0]) for color in colors_rgb]
colors_rgbw.append((0, 0, 0, 255))

# uncomment colors_rgbw if you have RGBW strip
colors = colors_rgb
# colors = colors_rgbw
brightness = 255
strip.brightness(brightness)



def rainbow():
    step = round(numpix / len(colors))
    current_pixel = 0
    strip.brightness(50)
    for color1, color2 in zip(colors, colors[1:]):
        strip.set_pixel_line_gradient(current_pixel, current_pixel + step, color1, color2)
        current_pixel += step
        time.sleep(0.5)
    strip.set_pixel_line_gradient(current_pixel, numpix - 1, violet, red)

def colour(r, g, b):
    strip.brightness(50)
    strip.set_pixel_line(0, (numpix - 1), (r, g, b))
        
        
def clear():
    strip.set_pixel_line(0, (numpix - 1), (0, 0, 0))
        
rainbow()



