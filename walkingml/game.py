from PIL import Image
import time
import pyautogui
from mss import mss


def capture_screenshot():
    # Capture entire screen
    with mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')



Image.open(capture_screenshot())



# Grab top-left rectangle with size 640px wide by 480px tall

time_passed = 5
for i in range(time_passed):
    print(f'Starting recording in {time_passed - i} seconds')
    time.sleep(1)


'''
while True:

    
    img = capture_screenshot()

    
    check_pixel = img.getpixel((330,222))
    print(check_pixel)
    if check_pixel == ((135, 96, 149)):
        print('Game Over')
        game_over = True              
    else:
        game_over = False 
    

    



    if game_over:  

        pyautogui.click((1128, 676   ))


    pyautogui.press('space')


 


       '''