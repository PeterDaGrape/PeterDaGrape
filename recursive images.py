from PIL import Image,ImageDraw
import math
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

w = 1400
h = 800

def draw_recursive(recursive_depth, length, length_ratio, angle, angle_change, start_x, start_y):

    if length < 1:
        
        return recursive_depth
    if recursive_depth >= max_recursion:
        return recursive_depth

    stop_x = start_x + math.sin(angle) * length
    stop_y = start_y + math.cos(angle) * length

    draw.line((start_x, start_y, stop_x, stop_y))

    level1 = draw_recursive(recursive_depth + 1, length * length_ratio, length_ratio, angle + angle_change, angle_change, stop_x, stop_y)
    level2 = draw_recursive(recursive_depth + 1, length * length_ratio, length_ratio, angle - angle_change, angle_change, stop_x, stop_y)

    return (level1 + level2) / 2
start_angle = math.pi /2

start_length = h / 4

max_recursion = 16

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((w, h))

def show_image(image):
    mode = image.mode
    size = image.size
    data = image.tobytes()

    return pygame.image.fromstring(data, size, mode)

angle_slider = Slider(screen, 0, 100, w, 20, min=0, max=180, step=1)
angle_output = TextBox(screen, 475, 160, 100, 40, fontSize=30)


ratio_slider = Slider(screen, 0, 80, w, 20, min=0, max=1.001, step=0.001)
ratio_output = TextBox(screen, 475, 200, 100, 40, fontSize=30)

recursion_output = TextBox(screen, 100, 130, 100, 40, fontSize=30)

ratio_output.disable()  # Act as label instead of textbox
angle_output.disable()
recursion_output.disable()

def call_recursion():

    level1 = draw_recursive(0, start_length, length_ratio, start_angle, angle_change, w / 2, h / 2)
    level2 = draw_recursive(0, start_length, length_ratio, start_angle + math.pi, angle_change, w / 2, h / 2)

    return (level1 + level2) / 2

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    image = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(image)

    angle_output.setText(angle_slider.getValue())
    ratio_output.setText(ratio_slider.getValue())

    length_ratio = ratio_slider.getValue()
    angle_change = math.radians(angle_slider.getValue())

    depth = call_recursion()

    recursion_output.setText(int(depth))

    screen.blit(source=show_image(image), dest=(0,0))

    pygame_widgets.update(events)
    pygame.display.update()

    clock.tick(60)