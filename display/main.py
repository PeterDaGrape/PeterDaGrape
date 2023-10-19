import sys
import os
from datetime import datetime

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
    global num_updates, full_update_i
    
    
    inverted_image = ImageOps.invert(window)
    if num_updates % full_update_i == 0:
        print('Initializing Full Update')

        epd.init(epd.FULL_UPDATE)
        epd.displayPartBaseImage(epd.getbuffer(inverted_image))
        epd.init(epd.PART_UPDATE)
        print('Fully Refresh Finished')
        
    else:
        print('Initializing Quick Update')
        
        epd.displayPartial(epd.getbuffer(inverted_image))

        print('Quick Refresh Finished')
    
    num_updates += 1

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
            ui.alarm()

    def core(self):
        global update_required
        
        #top bar and menu name
        self.draw.line((0, self.line_height, w, self.line_height), fill=(255,255,255), width=1)
        self.draw.text(text = self.current_window, xy = (w / 2, 0), anchor='mt', font = self.font)
        
        self.draw.text(text = 'Back', xy = (3, 1), anchor='lt', font = self.font)

        
        
        if touch_y > h - self.line_height and touch_y >= 0:
            print('Back')
            self.current_window = 'Main Menu'

            ui.Main_Menu()
            update_required = True
             
    def Main_Menu(self):
        
        global update_required, window

        
        self.draw.line((0, h - self.line_height, w, h - self.line_height), fill=(255,255,255), width=1)
              
        self.draw.text(text = get_time('%H:%M %d/%m/%y'), xy = (0, h), anchor = 'lb', font = self.font)
        
        num_buttons = 2
        
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
                
                self.window.paste(icon,(icon_x, icon_y))

            if i == 1:
                text = 'Alarm'




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


                
                update_required = True
                
            else:
                button_tapped = -1    
            
    def alarm(self):

        self.draw.text(text = alarm.alarm_time, xy=(ui.window_h / 2, w / 4), font=alarm.time_font, anchor='mm')

        self.draw.line((w / 2, self.line_height, w / 2, h))
       
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

class Alarm:
    def __init__(self):

        self.alarm_time = '00:00'
        self.time_font = ImageFont.truetype(fontdir, 30, encoding="unic")
        self.alarm_on = False


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

