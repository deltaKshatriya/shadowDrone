import ps_drone
import time, sys

command_interval = 0.10
deadband = 15


def compass_map_drone(x, y):
  if x == 0:
    return y * (180.0 / 100.0)
  return (x / abs(x)) * (abs(y) * (180.0 / 100.0))
  
def rotate_to(target, theta):
  diff = target - theta
  if diff > 180:
    diff -= 360
  if diff < -180:
    diff += 360
  print(diff)
  if diff > deadband:
    drone.turnRight(0.5)
    time.sleep(command_interval)
    drone.stop()
    return False
  elif diff < -deadband:
    drone.turnLeft(0.5)
    time.sleep(command_interval)
    drone.stop()
    return False
  else:
    return True
    
drone = ps_drone.Drone()
drone.startup()
drone.reset()                                      # Sets drone's status to good
while (drone.getBattery()[0] == -1):  time.sleep(0.1) 

drone.useDemoMode(False)                           # Give me everything...fast
drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"]) # Packets to decoded
print("Init complete, now resting")
time.sleep(0.5)  

print("Begin take off")
drone.takeoff() 

end = False
while not end:
  m = drone.NavData["magneto"][0]
  theta = compass_map_drone(m[0], m[1])
  print(theta)
  try:
    text = input()
    target = int(text)
    while not rotate_to(target, theta):
      m = drone.NavData["magneto"][0]
      theta = compass_map_drone(m[0], m[1])
  except ValueError:
    break

print("Landing")
drone.land()