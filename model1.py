# import the necessary packages
from social_distance_detector.pyimagesearch import social_distancing_config as config
from social_distance_detector.pyimagesearch.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import imutils
import cv2
import os
import time

def detect(obj):
	# decode the frame from its bytes form
	jpg_as_np = np.frombuffer(obj, dtype=np.uint8)
	frame = cv2.imdecode(jpg_as_np, flags=1)

	# resize the frame and then detect people (and only people) in it
	frame = imutils.resize(frame, width=700)
	results = detect_people(frame, config.net, config.ln,
		personIdx=config.LABELS.index("person"))

	# initialize the set of indexes that violate the minimum social
	# distance
	violate = set()

	# ensure there are *at least* two people detections (required in
	# order to compute our pairwise distance maps)
	if len(results) >= 2:
		# extract all centroids from the results and compute the
		# Euclidean distances between all pairs of the centroids
		centroids = np.array([r[2] for r in results])
		D = dist.cdist(centroids, centroids, metric="euclidean")

		# loop over the upper triangular of the distance matrix
		for i in range(0, D.shape[0]):
			for j in range(i + 1, D.shape[1]):
				# check to see if the distance between any two
				# centroid pairs is less than the configured number
				# of pixels
				if D[i, j] < config.MIN_DISTANCE:
					# update our violation set with the indexes of
					# the centroid pairs
					violate.add(i)
					violate.add(j)

	# loop over the results
	for (i, (prob, bbox, centroid)) in enumerate(results):
		# extract the bounding box and centroid coordinates, then
		# initialize the color of the annotation
		(startX, startY, endX, endY) = bbox
		(cX, cY) = centroid
		color = (0, 255, 0)

		# if the index pair exists within the violation set, then
		# update the color
		if i in violate:
			color = (0, 0, 255)

		# draw (1) a bounding box around the person and (2) the
		# centroid coordinates of the person,
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
		cv2.circle(frame, (cX, cY), 5, color, 1)

	# draw the total number of social distancing violations on the
	# output frame
	text = "Social Distancing Violations: {}".format(len(violate))
	cv2.putText(frame, text, (10, frame.shape[0] - 25),
		cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

	if len(violate)!=0:
		name = 1 + config.frame_num
		path = "/home/aravind/Desktop/RTSP_Streams/Spark/static/model1"
		cv2.imwrite(os.path.join(path,"{}.jpg".format(name)),frame)
		config.frame_num += 1

	# return the frame converted to bytes
	ret,encodedFrame = cv2.imencode('.jpg',frame)
	return encodedFrame.tobytes()