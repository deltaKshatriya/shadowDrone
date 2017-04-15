#!/usr/bin/env python

import sys
import time
from Queue import Queue
from gyroGesture import gyroGesture
from gesture import gesture
import gesture
from AnalogIO import AnalogIO
import socket

import ps_drone

TCP_IP = '192.168.7.2'
TCP_PORT = 5005
BUFFER_SIZE = 20
ENABLE_DRONE = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

if ENABLE_DRONE:
  drone = ps_drone.Drone()
  drone.startup()

# Gyro input
G = gyroGesture()
G.initialize()
# Number of static gestures to sequence
max_length = 3
# Time interval (in seconds) between static gestures
interval = 0.1
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
                gesture.CLOSED_PALM_UP]
    
def rotate_to(dir):
  if ENABLE_DRONE:
    
  
def perform_go():
  print("Go")
  x,y,z = G.bno.read_magnetometer()
  dir = compass_map(y, z)
  done = rotate_to(dir)
def perform_come():
  print("Come")
  x,y,z = G.bno.read_magnetometer()
  dir = compass_map(y, z)
  print((y, z))
  print(-dir)
def perform_lift_off():
  if ENABLE_DRONE:
    drone.takeoff()
  print("Lift off")
def perform_land():
  print("Land")
  if ENABLE_DRONE:
    drone.land()
  
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
  )                                \
]

mask_list    = [(0,0,0),(0,1,1),(0,1,1),(0,1,1),(0,1,1),(0,1,1),(0,1,1)]
discrepency_list = [0, 0, 0, 0, 0, 0, 0]
threshold_list = [2.0, 5.0, 5.0, 5.0, 4.0, 5.0, 5.0]

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
                comp[0]()
                dynamic_list[:] = []
                break
          
    time.sleep(interval)
except KeyboardInterrupt:
  s.close()