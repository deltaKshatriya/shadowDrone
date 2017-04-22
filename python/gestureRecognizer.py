#!/usr/bin/env python

import sys
import time
from Queue import Queue
from gyroGesture import gyroGesture
from gesture import gesture
import gesture
from AnalogIO import AnalogIO
import socket
import math

import ps_drone

TCP_IP = '192.168.7.2'
TCP_PORT = 5005
BUFFER_SIZE = 20
ENABLE_DRONE = False
MOVEMENT_SPEED = 0.4

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

if ENABLE_DRONE:
  drone = ps_drone.Drone()
  drone.startup()
  drone.reset()
  time.sleep(1.0)
  drone.useDemoMode(False)
  drone.getNDpackage(["demo","pressure_raw","altitude","magneto","wifi"])
  print "Battery: " + str(drone.getBattery()[0]) + "% " + str(drone.getBattery()[1])

# Gyro input
G = gyroGesture()
G.initialize()
# Number of static gestures to sequence
max_length = 3
# Time interval (in seconds) between static gestures
interval = 0.1
# Time interval between command updates to drone
command_interval = 0.10
deadband = 15
# Timeout in seconds
max_time = 10000.0
# Maximum allowable time between static positions
max_gap = 1

fingers = AnalogIO("AnalogConfig.json")

gesture_list = [gesture.POINTING, \
                gesture.OPEN_PALM_UP_RISING, \
                gesture.OPEN_PALM_UP_FALLING, \
                gesture.OPEN_PALM_DOWN_RISING, \
                gesture.OPEN_PALM_DOWN_FALLING, \
                gesture.OPEN_PALM_UP, \
                gesture.CLOSED_PALM_UP, \
                gesture.CLOSED_FIST_UP, \
                gesture.CLOSED_FIST_DOWN]

mask_list    = [(0,0,0),(0,1,1),(0,1,1),(0,1,1),(0,1,1),(0,1,1),(0,1,1),(0,1,1),(0,1,1)]
discrepency_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
threshold_list = [2.0, 6.0, 5.0, 5.4, 5.4, 5.0, 4.0, 2.5, 2.5]
  
def rotate_to(target, theta):
  diff = target - theta + 90
  while abs(diff) > 180:
    if diff > 180:
      diff -= 360
    if diff < -180:
      diff += 360
  print(diff)
  if diff > deadband:
    drone.turnRight(0.4)
    return False
  elif diff < -deadband:
    drone.turnLeft(0.4)
    return False
  else:
    return True
    
  
def perform_go():
  print("Go")
  x,y,z = G.bno.read_magnetometer()
  dir = compass_map(y, z)
  if ENABLE_DRONE:
    m = drone.NavData["magneto"][0]
    theta = compass_map_drone(m[0], m[1])
    complete = True#rotate_to(dir, theta)
    if complete:
      drone.moveForward(0.15)
      #drone.stop()
  # x_com = y / 10
  # x_com = 1 if x_com > 1 else (-1 if x_com < -1 else x_com)
  # y_com = math.sin(math.acos(x_com))
  # print((x_com, y_com))
  # if ENABLE_DRONE:
    # x_com *= MOVEMENT_SPEED
    # y_com *= MOVEMENT_SPEED
    # drone.move(x_com, y_com, 0, 0)
    # time.sleep(0.1)
    # drone.stop()
    
def perform_come():
  print("Come")
  x,y,z = G.bno.read_magnetometer()
  dir = compass_map(y, z)
  if ENABLE_DRONE:
    drone.moveBackward(0.15)
  
def perform_lift_off():
  if ENABLE_DRONE:
    drone.takeoff()
  print("Lift off")
  
def perform_land():
  print("Land")
  if ENABLE_DRONE:
    drone.land()
    
def perform_rise():
  print("Rise")
  if ENABLE_DRONE:
    drone.moveUp(0.5)
    time.sleep(command_interval)
    drone.stop()
    
def perform_fall():
  print("Fall")
  if ENABLE_DRONE:
    drone.moveDown(0.5)
    time.sleep(command_interval)
    drone.stop()
  
composite_list = [                 \
  (                                \
    perform_go,              \
    [                              \
      gesture.POINTING, \
    ]                              \
  ),                               \
  (                                \
    perform_lift_off,              \
    [                              \
      gesture.OPEN_PALM_UP_RISING, \
      gesture.OPEN_PALM_UP_FALLING \
    ]                              \
  ),                               \
  (                                \
    perform_land,                  \
    [                              \
      gesture.OPEN_PALM_DOWN_FALLING,\
      gesture.OPEN_PALM_DOWN_RISING  \
    ]                              \
  ),                                  \
  (                                \
    perform_come,                  \
    [                              \
      gesture.OPEN_PALM_UP,\
      gesture.CLOSED_PALM_UP  \
    ]                              \
  ),                               \
  (                                \
    perform_rise,                  \
    [                              \
      gesture.CLOSED_FIST_UP  \
    ]                              \
  ),                               \
  (                                \
    perform_fall,                  \
    [                              \
      gesture.CLOSED_FIST_DOWN  \
    ]                              \
  )                                \
]

winning_gesture = -1

# Enqueue a value, respecting the maximum queue size constraints
def enqueue(q, x):
  if q.qsize() >= max_length:
      q.get()
  q.put(x)
        
def compass_map(dir, parity):
  if dir > 0:
    if parity > -10:
      dir = (80 - abs(dir)) * (1 if dir > 0 else -1)
    dir *= 180.0 / 80.0
  if dir < 0:
    if parity > 0:
      dir = (80 - abs(dir)) * (1 if dir > 0 else -1)
    dir *= 180.0 / 80.0
  return dir
  
def compass_map_drone(x, y):
  if x == 0:
    return y * (180.0 / 100.0)
  return (x / abs(x)) * (abs(y) * (180.0 / 100.0))
        
static_queue = Queue()
dynamic_list = []
last_update = time.time()
try:
  # Enqueue the current position, then update the discrepency values
  # accordingly.
  # TODO: More accurate time-keeping
  for x in range(int(max_time / interval)):
    enqueue(static_queue, [  \
      G.getOrientation(),    \
      G.getAccel(),          \
      fingers.get_scaled(0), \
      fingers.get_scaled(1), \
      fingers.get_scaled(2), \
      fingers.get_scaled(3)])
        
    if (static_queue.qsize() == max_length):
      for i in range(len(gesture_list)):
        g = gesture_list[i]
        m = mask_list[i]
        t = 0
        d = 0
        for static in list(static_queue.queue):
          d += g.discrepency(static, t, m)
          t += interval
        discrepency_list[i] = d / threshold_list[i]
      if min(discrepency_list) < 1.0:
        winning_gesture = discrepency_list.index(min(discrepency_list))
        x = 0
        new_update = time.time()
        if new_update - last_update > max_gap:
          dynamic_list[:] = []
        if len(dynamic_list) == 0 or dynamic_list[-1] is not gesture_list[winning_gesture]:
          dynamic_list.append(gesture_list[winning_gesture])
          last_update = new_update
          print([item.name for item in dynamic_list])
        for comp in composite_list:
          if gesture.POINTING in comp and gesture.POINTING in dynamic_list:
            comp[0]()
            break
            
          for start in range(len(dynamic_list)):
            if len(comp[1]) <= len(dynamic_list) - start:
              for i in range(start, len(dynamic_list)):
                if dynamic_list[i] is not comp[1][i-start]:
                  break
              else:
                if gesture.OPEN_PALM_UP in dynamic_list:
                  dynamic_list[:] = [gesture.OPEN_PALM_UP]
                else:
                  dynamic_list[:] = []
                comp[0]()
                break
      elif ENABLE_DRONE:
        drone.stop()
    time.sleep(interval)
except KeyboardInterrupt:
  s.close()
  