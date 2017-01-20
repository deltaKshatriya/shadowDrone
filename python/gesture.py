import logging
import sys
import time
from gyroGesture import gyroGesture

# TODO: Incorporate finger positions

class gesture:
    heading_i = 0.0
    roll_i = 0.0
    pitch_i = 0.0
    
    x_rotvel = 0.0
    y_rotvel = 0.0
    z_rotvel = 0.0

    # initial: a triple of heading, roll, pitch denoting the
    # initial position
    # rotvel: a triple of x, y, and z rotational velocity
    def __init__(self, initial, rotvel):
        self.heading_i, self.roll_i, self.pitch_i = initial
        self.x_rotvel, self.y_rotvel, self.z_rotvel = rotvel
        
    # Returns a tuple of the projected gesture position after
    # the given number of seconds.
    # TODO: Determine if rotvel is correctly combined with initial.
    def extrapolate(self, seconds):
        return ( \
          self.heading_i + x_rotvel * seconds, \
          self.roll_i + y_rotvel * seconds,    \
          self.pitch_i + z_rotvel * seconds    \
        )
        
    # Returns the discrepency of the extrapolated static gesture
    # to the actual gesture after a given amount of time, masked
    # by a triple denoting whether to consider heading, roll, and/or
    # pitch. (Averaged over all considered dimensions.)
    def discrepency(self, actual, seconds, mask):
        h, r, p = self.extrapolate(seconds)
        dh = abs(h - actual.heading) * mask[0]
        dr = abs(r - actual.roll) * mask[1]
        dp = abs(p - actual.pitch) * mask[2]
        d = (dh + dr + dp) / (mask[0] + mask[1] + mask[2])
        return d
        