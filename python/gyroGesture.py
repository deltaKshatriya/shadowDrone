import logging
import sys
import time

from Adafruit_BNO055 import BNO055

class gyroGesture:
  heading = 0.0
  roll = 0.0
  pitch = 0.0
  bno = BNO055.BNO055(rst='P9_12')

  def initialize(self):
    self.bno = BNO055.BNO055(rst='P9_12')
    self.bno.begin()

  def getOrientation(self): 
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = self.bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    # sys, gyro, accel, mag = self.bno.get_calibration_status()
    return [heading, roll, pitch]
    
  def getAccel(self):
    x, y, z = self.bno.read_accelerometer()
    return [x, y, z]