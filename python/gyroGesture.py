import logging
import sys
import time

from Adafruit_BNO055 import BNO055
from enum import Enum

class gyroGesture:
	heading = 0.0
	roll = 0.0
	pitch = 0.0
	sys = 0.0
	gyro = 0.0
	accel = 0.0
	mag = 0.0
	bno = BNO055.BNO055(rst='P9_12')

	def initialize:
		bno = BNO055.BNO055(rst='P9_12')

	def getOrientation: 
		# Read the Euler angles for heading, roll, pitch (all in degrees).
		heading, roll, pitch = bno.read_euler()
		# Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    	sys, gyro, accel, mag = bno.get_calibration_status()
    	return [heading, roll, pitch]

    #TODO: Add means of discretizing the orientations so that we can actually do position recognition
