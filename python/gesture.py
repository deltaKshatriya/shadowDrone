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
    
    x_accel = 0.0
    y_accel = 0.0
    z_accel = 0.0
    
    fingers = [0.0, 0.0, 0.0, 0.0]

    # initial: a triple of heading, roll, pitch denoting the
    # initial position
    # rotvel: a triple of x, y, and z rotational velocity
    # accel: a triple of x, y, and z linear acceleration
    # fingers: a quad of finger positions [0-1]
    def __init__(self, name, initial, rotvel, accel, fingers):
      self.name = name
      self.heading_i, self.roll_i, self.pitch_i = initial
      self.x_rotvel, self.y_rotvel, self.z_rotvel = rotvel
      self.x_accel, self.y_accel, self.z_accel = accel
      self.fingers = fingers
        
    # Returns a tuple of the projected gesture position after
    # the given number of seconds.
    # TODO: Determine if rotvel is correctly combined with initial.
    def extrapolate(self, seconds):
      return ( \
        self.heading_i + self.x_rotvel * seconds, \
        self.roll_i + self.y_rotvel * seconds,    \
        self.pitch_i + self.z_rotvel * seconds    \
      )
    
    def _finger_discrepency(self, actual):
      f1 = 1 - abs(self.fingers[0] - actual[0])
      f2 = 1 - abs(self.fingers[1] - actual[1])
      f3 = 1 - abs(self.fingers[2] - actual[2])
      f4 = 1 - abs(self.fingers[3] - actual[3])
      f = 1 - f1 * f2 * f3 * f4
      return f
      
    def _360_dif(self, x, y):
      d = abs(x - y)
      if d > 180:
        return d - 180
      else:
        return d
        
    # Returns the discrepency of the extrapolated static gesture
    # to the actual gesture after a given amount of time, masked
    # by a triple denoting whether to consider heading, roll, and/or
    # pitch. (Averaged over all considered dimensions. Actual gesture
    # should be a list of gyro position, list of accel, followed by four finger
    # positions.)
    def discrepency(self, actual, seconds, mask):
      h, r, p = self.extrapolate(seconds)
      dh = self._360_dif(h, actual[0][0]) * mask[0]
      dr = self._360_dif(r, actual[0][1]) * mask[1]
      dp = self._360_dif(p, actual[0][2]) * mask[2]
      dax = abs(self.x_accel - actual[1][0])
      day = abs(self.y_accel - actual[1][1])
      daz = abs(self.z_accel - actual[1][2])
      f = self._finger_discrepency(actual[2:])
      #print(f)
      d = (dh + dr + dp) / (mask[0] + mask[1] + mask[2])
      da = dax + day + daz
      return d + da + f
        