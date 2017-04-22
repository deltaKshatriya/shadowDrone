import cv2
import numpy as np
import ps_drone

#takes previous frame and next frame as arguments
#calculates the optical flow and returns 
def calcOpticalFlow(prev, next):
	#threshold the images so that we can perform optical flow
	prevThresh = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
	nextThresh = cv2.cvtColor(next, cv2.COLOR_BGR2GRAY)

	#calculate flow
	flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

	return flow


#calculates best obstacle avoidance strategy
def obstacleAvoidRecommendation(prev, next):
	#first we need to calculate flow in different parts of image
	#for now, we sum all optical flow in the image
	flow = calcOpticalFlow(prev, next)
	sum = 0.0
	for row in flow:
		for vector in row:
			sum = sum + (vector[0] * vector[0]) + (vector[1] * vector[1])
	print sum
