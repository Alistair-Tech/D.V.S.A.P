import sys
import json
import base64
import time
import cv2
import numpy as np
from kafka import KafkaProducer
from multiprocessing import Process
import pymongo
import imutils
from datetime import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase"]

table = mydb["camera_urls"]

camera_urls = [str(d['link']) for d in table.find({},{"_id":0})]

print(camera_urls)


# rtsp links statically initialized
# camera_urls = ["rtsp://localhost:8554/video","example_01.mp4"]

# topic to write to
topic="video"

class StreamVideo(Process):
	
	def __init__(self,video_path,cam_num):
		"""
			  Video Streaming Producer Process Class. Publishes frames from a video source to a topic.
			  :param video_path: video url(rtsp)
			  :param cam_num: used in key to determine partition
		"""
		super(StreamVideo,self).__init__()
		self.video_path=video_path
		self.cam_num=cam_num

	def run(self):
		""" Publish video frames as bytes """
		
		# Producer Object
		producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
		# 												  value_serializer=lambda value: json.dumps(value).encode())

		camera = cv2.VideoCapture(self.video_path)

		frame_num = -1
		# Read frame-by-frame and publish
		while True:
			frame_num += 1
			success,frame = camera.read()
			if success == False:
				print("Error reading frame")
				break
			if frame_num % 8 != 0:
				continue
			frame = imutils.resize(frame, width=700)
			timeStamp = "Time: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
			cv2.putText(frame, timeStamp, (10, frame.shape[0] - 70),
					cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)
			string = cv2.imencode('.jpg', frame)[1]
			producer.send(topic,partition=self.cam_num,value=string.tobytes())
			time.sleep(0.5)

		camera.release()

# Init StreamVideo processes, these publish frames from respective camera to the same topic
PRODUCERS = [StreamVideo(url,index) for index,url in enumerate(camera_urls)]

# Start Publishing frames from cameras to the frame topic
for p in PRODUCERS:
	p.start()
	
# wait for producer processes to end
for p in PRODUCERS:
	p.join()