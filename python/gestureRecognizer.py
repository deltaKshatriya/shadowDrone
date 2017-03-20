import sys
import time
from Queue import Queue
from gyroGesture import gyroGesture
from gesture import gesture
import gesture
from AnalogIO import AnalogIO

# Gyro input
G = gyroGesture()
G.initialize()
# Number of static gestures to sequence
max_length = 3
# Time interval (in seconds) between static gestures
interval = 0.1
# Timeout in seconds
max_time = 10000.0
# Maximum allowable discrepency before a gesture is recognized
threshold = 3.75
# Maximum allowable time between static positions
max_gap = 1.0

fingers = AnalogIO("AnalogConfig.json")

gesture_list = [gesture.OPEN_PALM_UP_RISING, \
                gesture.OPEN_PALM_UP_FALLING, \
                gesture.OPEN_PALM_DOWN_RISING, \
                gesture.OPEN_PALM_DOWN_FALLING]
                
def perform_lift_off():
  print("Lift off")
def perform_land():
  print("Land")
  
composite_list = [                 \
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
  )                                \
]

mask_list    = [(0,1,1), (0,1,1)]
discrepency_list = [0, 0]

winning_gesture = -1

# Enqueue a value, respecting the maximum queue size constraints
def enqueue(q, x):
  if q.qsize() >= max_length:
      q.get()
  q.put(x)
        
static_queue = Queue()
dynamic_list = []
last_update = time.time()

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
      discrepency_list[i] = d
    if (min(discrepency_list) < threshold):
      winning_gesture = discrepency_list.index(min(discrepency_list))
      x = 0
      new_update = time.time()
      if new_update - last_update > max_gap:
        dynamic_list[:] = []
        if len(dynamic_list) == 0 or dynamic_list[-1] is not gesture_list[winning_gesture]:
          dynamic_list.append(gesture_list[winning_gesture])
          print(winning_gesture)
        for comp in composite_list:
          if len(comp[1]) == len(dynamic_list):
            for real, target in zip(dynamic_list, comp[1]):
              if real is not target:
                break
            else:
              comp[0]()
      last_update = new_update
        
  time.sleep(interval)