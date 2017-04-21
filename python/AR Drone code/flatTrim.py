import ps_drone
import time, sys

drone = ps_drone.Drone()
# drone.reset()                                      # Sets drone's status to good
# while (drone.getBattery()[0]==-1): time.sleep(0.1) # Wait until drone has done its reset
# print "Battery: " + str(drone.getBattery()[0]) + "% " + str(drone.getBattery()[1]) # Battery-status
# drone.useDemoMode(False)                           # Give me everything...fast
# drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"]) # Packets to decoded
drone.startup()
print("Init complete, now resting")
time.sleep(0.5)  



# while True:
# 	while drone.NavDataCount==NDC:
# 		drone.getNDPackage("all")



print("Begin f-trim")
drone.trim()
time.sleep(3)
print("f-trim complete, resting")