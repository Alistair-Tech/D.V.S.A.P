from flask import Flask, Response, render_template
from kafka import KafkaConsumer, TopicPartition
import os

# # topic to read the processed frames from
# topic = 'spark'

# Set the consumer in a Flask App
app = Flask(__name__)

# # route to display stream of one camera
# @app.route("/cam/<int:cam_num>")
# def cam(cam_num):
# 	consumer = KafkaConsumer(bootstrap_servers = ['localhost:9092'])

# 	consumer.assign([TopicPartition(topic = topic, partition = cam_num-1)])

# 	return Response(get_video_stream(consumer),
# 		mimetype='multipart/x-mixed-replace; boundary=frame')

# def get_video_stream(consumer):
# 	for msg in consumer:
# 		yield (b'--frame\r\n'
#                    b'Content-Type: image/jpg\r\n\r\n' + msg.value + b'\r\n\r\n')

@app.route("/getViolations")
def getViolations():
	images = os.listdir('static/model1')
	images.sort(key = lambda name: int(name[0:-4]))
	images = ['model1/' + file for file in images]
	return render_template('violations.html', images = images)

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 3000, debug = True)
