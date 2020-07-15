import sys
from flask import Flask, Response, render_template, request, redirect
from kafka import KafkaConsumer, TopicPartition

# topic name
topic = 'video'

# number of modules
N = 3
m = [[]]*N

# setting the consumer in a flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("homepage.html")

@app.route('/module/<int:mno>', methods=['GET', 'POST'])
def module(mno):
    global m
    mno -= 1
    if request.method == 'POST':
        m[mno] = request.form.getlist('module')
        for item in m[mno]:
            item = int(item)
        print(m[mno])
    return render_template("module.html", cam_nums=m[mno], mno=mno)

@app.route('/cam/<camno>')
def cam(camno):
    consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'])
    consumer.assign([TopicPartition(topic = topic, partition = int(camno))])

    return Response(
        get_video(consumer), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/all/<camera_numbers>")
def get_cameras(camera_numbers):
    return render_template("videos.html", cam_nums=list(range(int(camera_numbers))))

def get_video(consumer):
    for msg in consumer:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + msg.value + b'\r\n\r\n')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
