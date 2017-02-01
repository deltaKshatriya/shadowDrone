import logging
import sys
import time
from gyroGesture import gyroGesture

class gesture:
    heading_i = 0.0
    roll_i = 0.0
    pitch_i = 0.0
    
    x_rotvel = 0.0
    y_rotvel = 0.0
    z_rotvel = 0.0
    
    fingers = [0.0, 0.0, 0.0, 0.0]

    # initial: a triple of heading, roll, pitch denoting the
    # initial position
    # rotvel: a triple of x, y, and z rotational velocity
    # fingers: a quad of finger positions [0-1]
    def __init__(self, initial, rotvel, fingers):
        self.heading_i, self.roll_i, self.pitch_i = initial
        self.x_rotvel, self.y_rotvel, self.z_rotvel = rotvel
        self.fingers = fingers
        
    # Returns a tuple of the projected gesture position after
    # the given number of seconds.
    # TODO: Determine if rotvel is correctly combined with initial.
    def extrapolate(self, seconds):
        return ( \
          self.heading_i + x_rotvel * seconds, \
          self.roll_i + y_rotvel * seconds,    \
          self.pitch_i + z_rotvel * seconds    \
        )
    
    def _finger_discrepency(self, actual):
      f1 = 1 - abs(fingers[0] - actual[0])
      f2 = 1 - abs(fingers[1] - actual[1])
      f3 = 1 - abs(fingers[2] - actual[2])
      f4 = 1 - abs(fingers[3] - actual[3])
      f = 1 - f1 * f2 * f3 * f4
      return f
      
    # Returns the discrepency of the extrapolated static gesture
    # to the actual gesture after a given amount of time, masked
    # by a triple denoting whether to consider heading, roll, and/or
    # pitch. (Averaged over all considered dimensions. Actual gesture
    # should be a list of gyro position, followed by four finger
    # positions.)
    def discrepency(self, actual, seconds, mask):
        h, r, p = self.extrapolate(seconds)
        dh = abs(h - actual[0].heading) * mask[0]
        dr = abs(r - actual[0].roll) * mask[1]
        dp = abs(p - actual[0].pitch) * mask[2]
        f = _finger_discrepency(self, actual[1:])
        d = (dh + dr + dp) / (mask[0] + mask[1] + mask[2])
        return d + f
        