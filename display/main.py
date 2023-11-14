import sys
import os
from datetime import datetime

from pydub import AudioSegment
from pydub.playback import play

libdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
    
fontdir = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts'), 'Roboto-Bold.ttf')
icondir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')

from TP_lib import gt1151
from TP_lib import epd2in13_V4
import math
import time
from PIL import Image,ImageDraw,ImageFont, ImageOps
import threading


w = 250
h = 122

class touch:
    def __init__(self):
        self.old_x = 0
        self.old_y = 0
        
        self.x = 0
        self.y = 0

    def touch_daemon() :
        while flag_t == 1 :
            if(gt.digital_read(gt.INT) == 0) :
                GT_Dev.Touch = 1
            else:
                GT_Dev.Touch = 0
    
    def wait_touch(self):

        self.old_x = self.x
        self.old_y = self.y
        if self.x == self.old_x and self.y == self.old_y:
            gt.GT_Scan(GT_Dev, GT_Old)

            self.x = w - GT_Dev.Y[0]
            self.y = GT_Dev.X[0]
            return False

        print('Tapped', self.x, self.y)
        
        return (self.x, self.y)
            
def update_screen(window):
    inverted_image = ImageOps.invert(window)
    print('Initializing Full Update')
    epd.init(epd.FULL_UPDATE)

    epd.displayPartBaseImage(epd.getbuffer(inverted_image))
    print('Fully Refresh Finished')

def get_time(format):
    global old_time, update_required
    now = datetime.now()
    
    the_time = now.strftime(format)
    
    minutes = now.strftime('%M')
    if old_time != minutes:
        print('Time Changed')
        update_required = True
        old_time = minutes
        
    return the_time
    
class UI:
    def __init__(self, current_window):
        self.current_window = current_window
        self.font = ImageFont.truetype(fontdir, 10, encoding="unic")
        self.line_height = 10
        self.text_height = 15
        self.window_h = h - self.line_height

    def refresh_current(self):

        self.window = Image.new('RGB', (w, h))

        self.draw = ImageDraw.Draw(self.window)

        ui.core()

        if self.current_window == 'Main Menu':
            self.Main_Menu()
        if self.current_window == 'Clock':
            self.clock()
        if self.current_window == 'Alarm':
            self.alarm()
        if self.current_window == 'Mandelbrot':
            self.mandelbrot()

    def core(self):
        global update_required
        
        #top bar and menu name
        self.draw.line((0, self.line_height, w, self.line_height), fill=(255,255,255), width=1)
        self.draw.text(text = self.current_window, xy = (w / 2, 0), anchor='mt', font = self.font)
        
        self.draw.text(text = 'Back', xy = (3, 1), anchor='lt', font = self.font)

        if alarm.alarm_on:
            
            icon_dimensions = 10
            
            ringer = Image.open(os.path.join(icondir, 'clock.png')).resize((icon_dimensions, icon_dimensions))
            ringer = ImageOps.invert(ringer)

            self.window.paste(ringer,(w-icon_dimensions, 0))
        
        if touch_y > h - self.line_height and touch_y >= 0:
            print('Back')
            self.current_window = 'Main Menu'

            ui.Main_Menu()
            update_required = True
            
    def Main_Menu(self):
        
        global update_required, window

        self.draw.line((0, h - self.line_height, w, h - self.line_height), fill=(255,255,255), width=1)
              
        self.draw.text(text = get_time('%H:%M %d/%m/%y'), xy = (0, h), anchor = 'lb', font = self.font)
        
        num_buttons = 3
        
        button_spacing = int(w / num_buttons)
        
        for i in range(num_buttons + 1):
            
            y = h / 2
            x = (w / num_buttons * i)
            
            self.draw.line((x, self.line_height, x, h - self.line_height), fill=(255,255,255), width=1)
            self.draw.line(((i * button_spacing), h - self.text_height - self.line_height, (i + 1 * button_spacing), h - self.text_height - self.line_height), fill=(255,255,255), width=1)
            
            button_center_x = (i * button_spacing + (i+1) * button_spacing) / 2
            button_center_y = h - (self.line_height + self.text_height) + self.text_height / 2
            
            icon_space_ratio = 2
            
            icon_dimension = int(button_spacing / icon_space_ratio)
            
            icon_x = int((i * button_spacing + (i+1) * button_spacing) / 2 - (icon_space_ratio * (icon_dimension / 2)) / icon_space_ratio)
            icon_y = int(h - (self.line_height + self.text_height + self.line_height + h) / 4) - icon_dimension
            icon_y = int((self.line_height + self.text_height + self.line_height) /2)
            if i == 0:
                text = 'Clock'
                
                icon = Image.open(os.path.join(icondir, 'clock.png')).resize((icon_dimension, icon_dimension))
                
                
                icon = ImageOps.invert(icon)
            
            if i == 1:
                text = 'Alarm'

                icon = Image.open(os.path.join(icondir, 'ringer.png')).resize((icon_dimension, icon_dimension)).convert('RGB')
                icon = ImageOps.invert(icon)
            if i == 2:
                text = 'Mandelbrot'

            
            self.window.paste(icon,(icon_x, icon_y))

            self.draw.text(text = text, xy = (button_center_x, button_center_y),  anchor='mm', font = self.font)
        self.draw.line((w-1, self.line_height, w-1, h - self.line_height), fill=(255,255,255), width=1)

        for i in range(num_buttons):
            
            if (touch_x > i * button_spacing and touch_x < (i+1) * button_spacing) and (touch_y < h - self.line_height and touch_y > self.line_height):
                print('Tapped', i)
                button_tapped = i
                
                if button_tapped == 0:
                      
                    self.current_window = 'Clock'

                if button_tapped == 1:

                    self.current_window = 'Alarm'
                if button_tapped == 2:
                    self.current_window = 'Mandelbrot'
                    self.mandelbrot = Mandelbrot()

                update_required = True
                
            else:
                button_tapped = -1    
            
    def clock(self):
        global update_required

        big_font_size = 50
        big_font = ImageFont.truetype(fontdir, big_font_size, encoding="unic")
        
        center_x = w / 2
        center_y = (h - self.line_height) / 2 + self.line_height

        date = get_time('%d/%m/%y')
        minute_hours = get_time('%H:%M')
            
        self.draw.text(text = minute_hours, xy = (center_x, center_y - big_font_size / 2),  anchor='mm', font = big_font)
        self.draw.text(text = date, xy = (center_x, center_y + big_font_size / 2),  anchor='mm', font = big_font)

    def alarm(self):

        self.draw.text(text = f'{alarm.alarm_hours:02d}:{alarm.alarm_minutes:02d}', xy=(ui.window_h / 2, w / 4), font=alarm.time_font, anchor='mm')

        self.draw.line((w / 2, self.line_height, w / 2, h))

        triangle_h = 20
        triangle_w = 30

        arrow_distance = 20
        button_spacing = 40

        self.draw.polygon([((w / 4) + button_spacing / 2 ,  (h / 2) - (arrow_distance + triangle_h)), ((w / 4) + button_spacing / 2  + triangle_w / 2, (h / 2) - (arrow_distance)), ((w / 4) + button_spacing / 2  - triangle_w / 2, (h / 2) - (arrow_distance))]
                          , fill=(255,255,255))
        self.draw.polygon([((w / 4) + button_spacing / 2 ,  (h / 2) + (arrow_distance + triangle_h)), ((w / 4) + button_spacing / 2  + triangle_w / 2, (h / 2) + (arrow_distance)), ((w / 4) + button_spacing / 2  - triangle_w / 2, (h / 2) + (arrow_distance))]
                          , fill=(255,255,255))
        
        self.draw.polygon([((w / 4) - button_spacing / 2 ,  (h / 2) - (arrow_distance + triangle_h)), ((w / 4) - button_spacing / 2  + triangle_w / 2, (h / 2) - (arrow_distance)), ((w / 4) - button_spacing / 2  - triangle_w / 2, (h / 2) - (arrow_distance))]
                          , fill=(255,255,255))
        self.draw.polygon([((w / 4) - button_spacing / 2 ,  (h / 2) + (arrow_distance + triangle_h)), ((w / 4) - button_spacing / 2  + triangle_w / 2, (h / 2) + (arrow_distance)), ((w / 4) - button_spacing / 2  - triangle_w / 2, (h / 2) + (arrow_distance))]
                          , fill=(255,255,255))
        
        alarm.change_time()

        alarm_font = ImageFont.truetype(fontdir, 25, encoding="unic")

        if alarm.alarm_on:

            self.draw.text(xy = (3 * w / 4, self.window_h / 2) ,text='Alarm is \n Enabled', font = alarm_font, anchor='mm')
        else:
            self.draw.text(xy = (3 * w / 4, self.window_h / 2) ,text='Alarm is \n Disabled', font = alarm_font, anchor='mm')

        alarm.toggle_alarm()

    def mandelbrot(self):

        set = self.mandelbrot.calculate()

        self.window.paste(set, (0, self.line_height))

class Alarm:
    def __init__(self):
        
        self.alarm_path = '/home/pi/Python/display/audio.wav'
        self.sound = AudioSegment.from_wav(self.alarm_path)
        self.triggered = False
        self.alarm_hours = 6
        self.alarm_minutes = 55
        self.time_font = ImageFont.truetype(fontdir, 30, encoding="unic")
        self.alarm_on = False

    def change_time(self):
        global update_required

        if touch_x > 0 and touch_y > 0 and update_required != True:
            if touch_x < w / 2:

                if touch_x < w / 4:

                    if touch_y < ui.window_h / 2:
                        self.alarm_hours -= 1
                        update_required = True
                    if touch_y > ui.window_h / 2:
                        self.alarm_hours += 1
                        update_required = True

                if touch_x > w / 4:


                    if touch_y < ui.window_h / 2:
                        self.alarm_minutes -= 5
                        update_required = True
                    if touch_y > ui.window_h / 2:
                        self.alarm_minutes += 5
                        update_required = True
        if self.alarm_minutes >= 60:
            self.alarm_minutes -= 60
        if self.alarm_minutes < 0:
            self.alarm_minutes += 60        
        if self.alarm_hours >= 23:
            self.alarm_hours -= 24
        if self.alarm_hours < 0:
            self.alarm_hours += 24

    def toggle_alarm(self):
        global update_required

        if touch_x > 0 and touch_y > 0 and update_required != True:
            
            if touch_x > w / 2:
                if self.alarm_on:
                    self.alarm_on = False

                else:
                    self.alarm_on = True
                update_required = True
 
    def alarm_trigger(self):
        
        cur_minutes = get_time('%M')
        cur_hour = get_time('%H')

        if int(cur_minutes) == int(self.alarm_minutes):
            
            if int(cur_hour) == int(self.alarm_hours):
                if not self.triggered:
                    print('Alarm is triggered... ')
                    self.triggered = True

                    play(self.sound)

        else:
            self.triggered = False

class Mandelbrot:
    def __init__(self):
        self.w = w
        self.h = h - ui.line_height
        
        
        self.start_x = -2
        self.start_y = -1.2
        self.stop_x = 0.6
        self.stop_y = 1.2

        self.itermax = 100

        self.stepsize = (self.stop_y - self.start_y) / (self.h)
    def calculate(self):

        image = Image.new('RGB', (w, h))
        image_load = image.load()

        print('Calculating...')

        self.stop_x = self.stepsize * w + self.start_x
        
        global repeat, percentage
        percentage = 0
        repeat = 0
        
        xn = 0
        yn = 0
        yc = self.start_y
        xnplus1 = 0
        ynplus1 = 0
        imax = 0
        
        for ypix in range(h):
            xc = self.start_x
            for xpix in range(w):
                xn = 0
                yn = 0
                                    
                for i in range(self.iter_max):
                    xnplus1 = xn**2 - yn**2 + xc
                    ynplus1 = (2 * xn * yn) + yc
                    xn = xnplus1
                    yn = ynplus1
                    if imax < i:
                        imax = i
                    if xn*xn + yn*yn > 4:
                        break
                    #print(i)
                #print(i)

                if i < (self.iter_max - 1):
                    color = int(round(self.iter_max * (math.sqrt(i / self.iter_max))))
                    color = i * 15 % 255

                else:
                    color = 0
                #color = int(255 - (i / itermax) * 255)
                image_load[xpix, ypix] = (color, color, color)
                xc = (xc + self.stepsize)
            
            yc = (yc + self.stepsize)
            
            if not percentage == round((ypix / h) * 100):
                percentage = round((ypix / h) * 100)
                if percentage % 10 == 0:
                    print(percentage)

        return image

def main():
    
    global ui, alarm, update_required, touch_x, touch_y
    update_required = True
    alarm = Alarm()
    ui = UI('Main Menu')
    t = touch()
    old_touch_x = w
    old_touch_y = h

    while True:
        
        gt.GT_Scan(GT_Dev, GT_Old)
        touch_x = w - GT_Dev.Y[0]
        touch_y = h - GT_Dev.X[0]
        
        if old_touch_x != touch_x and old_touch_y != touch_y:
            old_touch_x = touch_x
            old_touch_y = touch_y
            print('Tap')
        else:
            touch_x = -1
            touch_y = -1
        
        ui.refresh_current()

        if alarm.alarm_on:
            alarm.alarm_trigger()
            
        if update_required:
               
            ui.refresh_current()
            
            print('Update required main')

            update_screen(ui.window)
            update_required = False

try:

    flag_t = 1
    epd = epd2in13_V4.EPD()
    gt = gt1151.GT1151()
    GT_Dev = gt1151.GT_Development()
    GT_Old = gt1151.GT_Development()
    
    t = touch()
    
    num_updates = 0
    full_update_i = 3

    old_time = 0
    
    epd.init(epd.FULL_UPDATE)
    
    gt.GT_Init()
    epd.Clear(0xFF)
    
    touch_thread = threading.Thread(target = touch.touch_daemon)
    touch_thread.setDaemon(True)
    touch_thread.start()

except KeyboardInterrupt:
    flag_t = 0
    epd.sleep()
    time.sleep(2)
    t.join()
    epd.Dev_exit()
    exit()

main()