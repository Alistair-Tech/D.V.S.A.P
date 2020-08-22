from flask import Flask, Response, render_template
from kafka import KafkaConsumer, TopicPartition
import os

# # topic to read the processed frames from
# topic = 'spark'

# Set the consumer in a Flask App
app = Flask(__name__)


@app.route("/getViolations")
def getViolations():
	images = os.listdir('static/model1')
	images.sort(key = lambda name: int(name[0:-4]))
	images = ['model1/' + file for file in images]
	return render_template('violations.html', images = images)

@app.route("/getCounts")
def getCounts():
	images = os.listdir('static/model2')
	images.sort(key = lambda name: int(name[0:-4]))
	images = ['model2/' + file for file in images]
	return render_template('counts.html', images = images)

if __name__ == "__main__":
	app.run(host = '0.0.0.0', port = 3000, debug = True)
