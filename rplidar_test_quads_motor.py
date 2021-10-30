"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

import time
import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar
import RPi.GPIO as io

io.setmode(io.BOARD)
pwm=18
io.setup(pwm,io.OUT)
p=io.PWM(pwm,100)
p.start(0)

# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((320,240))
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

# used to scale data to fit on the screen
max_distance = 0

#pylint: disable=redefined-outer-name,global-statement
def process_data(data):
    global max_distance
    lcd.fill((0,0,0))
    for angle in range(360):
        distance = data[angle]

               

        
        if distance > 0:                  # ignore initially ungathered data points
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            print(distance)
            dist(distance)
    

            if radians>=0 and radians<1.72:
                print("Object detected in First Quadrant")

            if radians>=1.72 and radians<3.14:
                print("Object detected in Second Quadrant")

            if radians>=3.14 and radians<5.16:
                print("Object detected in Third Quadrant")

            if radians>=5.16 and radians<6.28:
                print("Object detected in Fourth Quadrant")

            
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119)) 
            lcd.set_at(point, pygame.Color(255, 255, 255))

       # time.sleep(2) 
    pygame.display.update()
    

def dist(dis):
    if dis>1 and dis<=3000:
        print("Very near to Obstacle: RED zone")
        p.ChangeDutyCycle(30)
        

    elif dis>3000 and dis<=7000:
        print("Obstacle Approaching: BLUE zone")
        p.ChangeDutyCycle(50)

    elif dis>7000 and dis<=12000:
        print("No Obstacle: GREEN zone")
        p.ChangeDutyCycle(80)
#for i in range(0,500):
 #   pass
#time.sleep(2)        
p.stop()
scan_data = [0]*360



try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)

except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
