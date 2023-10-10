from colorwave import *
import utime
import _thread

clear()
utime.sleep(1)
rainbow()
def rotate():
    while True:
        strip.rotate_right(1)
        time.sleep(0.05)
        strip.show() 


#strip.rotate_right(30)
#strip.show()
_thread.start_new_thread(rotate, ())

