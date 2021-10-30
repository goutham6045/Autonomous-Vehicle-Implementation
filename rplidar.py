import time
import os
import sys
from math import cos, sin, pi
#from PIL import Image
import pygame
from rplidar import RPLidar
lidar = RPLidar(None,PORT_NAME)
try:
print('Recording measurments... Press Crl+C to stop.')
for scan in lidar.iter_scans():
pass
lcd.fill((0,0,0))
for (_, angle, distance) in scan:
max_distance = max([distance, max_distance])
radians = angle * pi / 180.0
x = distance * cos(radians)
y = distance * sin(radians)
point = (240 + int(x / max_distance * 159), 160 + int(y / max_distance * 159))
if(((angle>0 and angle<20) or (angle>340 and angle<360)) and distance<2000):
             lcd.set_at(point, pygame.Color(255, 0, 0))
             f.ChangeDutyCycle(0)
else:
      lcd.set_at(point, pygame.Color(255, 255, 255))
       f.ChangeDutyCycle(30)
pygame.display.update()

except KeyboardInterrupt:
         print('Stoping.')
        f.ChangeDutyCycle(0)
lidar.stop()
lidar.disconnect()
