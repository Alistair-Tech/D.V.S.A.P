import sys
import time
import cv2
from kafka import KafkaProducer

from multiprocessing import Process
import pymongo

#connect to database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["video"]
#collection
mycol = mydb["user"]
camera_urls = []

#retrieves data from database and makes the list of urls.
cursor = mycol.find({})
for document in cursor:
        camera_urls.append(document['url'])

# rtsp links statically initialized
# camera_urls = ["rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov",
# 					    "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"]

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
		producer = KafkaProducer(bootstrap_servers='localhost:9092')

		camera = cv2.VideoCapture(self.video_path)

		# Read frame-by-frame and publish
		try:
			while True:
				success,frame = camera.read()

				ret,buffer = cv2.imencode('.jpg',frame)

				# Publish to specific partition
				producer.send(topic,partition=self.cam_num,value=buffer.tobytes())

				time.sleep(0.2)

		except:
			print("\nExiting...")
			sys.exit(1)

		camera.release()

# Init StreamVideo processes, these publish frames from respective camera to the same topic
PRODUCERS = [StreamVideo(url,index) for index,url in enumerate(camera_urls)]

# Start Publishing frames from cameras to the frame topic
for p in PRODUCERS:
	p.start()
	
# wait for producer processes to end
for p in PRODUCERS:
	p.join()
