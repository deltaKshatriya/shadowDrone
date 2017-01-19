import sys
sys.path.insert(0, '/Users/kunalM/shadowDrone/shadowDrone/python/AR Drone code/python-ardrone')

import libardrone
from time import sleep

drone = libardrone.ARDrone()
drone.takeoff()
sleep(3)
drone.land()
sleep(3)
drone.halt()
