import ps_drone
import time, sys
import socket

TCP_IP = '192.168.7.2'
TCP_PORT = 5005
BUFFER_SIZE = 20

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((TCP_IP, TCP_PORT))

#s.listen(1)
#s.connect((TCP_IP, TCP_PORT))

#print('Connection address: ', addr)

drone = ps_drone.Drone()
# drone.reset()                                      # Sets drone's status to good
# while (drone.getBattery()[0]==-1): time.sleep(0.1) # Wait until drone has done its reset
# print "Battery: " + str(drone.getBattery()[0]) + "% " + str(drone.getBattery()[1]) # Battery-status
# drone.useDemoMode(False)                           # Give me everything...fast
# drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"]) # Packets to decoded
drone.startup()
drone.trim()
time.sleep(3)
drone.takeoff()
time.sleep(5)
drone.land()

# while True:
# 	data = s.recv(BUFFER_SIZE)
# 	if not data: break
# 	print("received data:", data)
# 	if (data == 'L'):
# 		#land
# 		print("HAHA! IT'S LANDING!")
# 		#drone.land()
# 	if (data == 'T'):
# 		#takeoff
# 		print("HAHA! IT'S TAKING OFF!")
# 		#drone.takeoff()

# s.close()

