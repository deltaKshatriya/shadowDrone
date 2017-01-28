import sys
import time
from Queue import Queue
from gyroGesture import gyroGesture
from gesture import gesture

# Gyro input
G = gyroGesture()
G.initialize
# Number of static gestures to sequence
max_length = 10
# Time interval (in seconds) between static gestures
interval = 0.1
# Timeout in seconds
max_time = 10.0
# Maximum allowable discrepency before a gesture is recognized
threshold = 100.0

# TODO: define real gestures
gesture_list = [gesture((0,0,0),(0,0,0))]
mask_list    = [(1, 1, 1)]
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
for range(max_time / interval):
    enqueue(static_queue, g.getOrientation())
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
        break
    time.sleep(interval)
    
printf "Winning gesture is %d with a discrepency of %f" % \
    winning_gesture, min_discrepency_list
        
        