import ps_drone

drone = ps_drone.Drone()
drone.startup()
drone.trim()

drone.setConfigAllID()
drone.sdVideo()
drone.frontCam()
CDC = drone.ConfigDataCount
while CDC==drone.ConfigDataCount: time.sleep(0.001) # Wait until it is done (after resync)
drone.startVideo()

prev = drone.VideoImage
next = drone.VideoImage
while 1:
	prev = next
	next = drone.VideoImage
	obstacleAvoidRecommendation(prev, next)