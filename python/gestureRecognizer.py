import sys
import time
from Queue import Queue
from gyroGesture import gyroGesture
from gesture import gesture
from AnalogIO import AnalogIO

# Gyro input
G = gyroGesture()
G.initialize()
# Number of static gestures to sequence
max_length = 10
# Time interval (in seconds) between static gestures
interval = 0.1
# Timeout in seconds
max_time = 10000.0
# Maximum allowable discrepency before a gesture is recognized
threshold = 100.0

fingers = AnalogIO("AnalogConfig.json")

# TODO: define real gestures
gesture_list = [gesture("placeholder", (0,0,0), (0,0,0), (0,0,0,0))]
mask_list    = [(0, 1, 1)]
discrepency_list = [0]

winning_gesture = -1

# Enqueue a value, respecting the maximum queue size constraints
def enqueue(q, x):
  if q.qsize() >= max_length:
      q.get()
  q.put(x)
        
static_queue = Queue()

# Enqueue the current position, then update the discrepency values
# accordingly.
# TODO: More accurate time-keeping
for x in range(int(max_time / interval)):
  enqueue(static_queue, [  \
    G.getOrientation(),    \
    fingers.get_scaled(0), \
    fingers.get_scaled(1), \
    fingers.get_scaled(2), \
    fingers.get_scaled(3)])
  print(fingers.get_scaled(0))
  print(fingers.get_scaled(2))
  print(fingers.get_scaled(3))
  print("----")
  #print(G.getOrientation())
  #print(gesture_list[0].discrepency([G.getOrientation(), 0, 0, 0, 0], 0, mask_list[0]))
      
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
      #break
  time.sleep(interval)
    
print "Winning gesture is %d with a discrepency of %f" % \
  (winning_gesture, min(discrepency_list))
        
        