import ps_drone
from time import sleep

drone = ps_drone.Drone()
drone.startup()
drone.takeoff() 
sleep(3)
drone.land()