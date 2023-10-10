import rp2

import network
import ubinascii
import machine
import time



rotatebool = False
'''
clear()
time.sleep(1)
rainbow()
'''



# Set country to avoid possible errors
rp2.country('GB')
print('im here')
SSID = "Crossacres"
PASSWD = "catocat3"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# If you need to disable powersaving mode
#wlan.config(pm = 0xa11140)
wlan.ifconfig(('192.168.68.121', '255.255.255.0', '192.168.68.1', '8.8.8.8'))


# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Other things to query
# print(wlan.config('channel'))
# print(wlan.config('essid'))
# print(wlan.config('txpower'))

# Load login data from different file for safety reasons


wlan.connect(SSID, PASSWD)

# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)
    
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth
if wlan.status() != 3:
    print(wlan.status())
    raise RuntimeError('Wi-Fi connection failed')
else:
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(wlan.status()):
        led.on()
        time.sleep(.1)
        led.off()
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# HTTP server with socket

import socket

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)







HOST = "192.168.68.121"
PORT = 39127

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind((HOST, PORT))
serv.listen(5)

from colorwave import *
import _thread


def rotate():
    while rotatebool == True:
        strip.rotate_right(1)
        time.sleep(0.05)
        strip.show()

_thread.start_new_thread(rotate, ())


while True:
    conn, addr = serv.accept()
    from_client = ''
    while True:
        rawdata = conn.recv(4096)
        data = rawdata.decode()
        if not data: break
        from_client += data
        print(from_client)
        
        if from_client == ('RAINBOW_ON'):
            print('LED ON')
            led.value(1)
            rainbow()
            _thread.start_new_thread(rotate, ())

            rotatebool = True
            strip.show()

        if from_client == ('CLEAR'):
            print('LED OFF')
            led.value(0)
            rotatebool = False
            clear()
            strip.show()

        if from_client == ('STOP'):
            exit()        

        if 'HEX' in from_client:
            hex = [int(s) for s in from_client.split() if s.isdigit()]
            print(hex)
            led.value(1)
            colour(hex[0], hex[1], hex[2])
            
            
            rotatebool = False
            
            strip.show()
            
        
        
        
        conn.send("RECEIVED")
    conn.close()
    print('client disconnected')
