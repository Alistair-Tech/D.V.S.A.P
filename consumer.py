
from flask import Flask, Response, render_template
from kafka import KafkaConsumer, TopicPartition

# Fire up the Kafka Consumer
topic = "video"


# Set the consumer in a Flask App
app = Flask(__name__)


# route to display stream of one camera
@app.route("/cam/<cam_num>")
def cam(cam_num):
    """
    This is the heart of our video display. Notice we set the mimetype to 
    multipart/x-mixed-replace. This tells Flask to replace any old images with 
    new values streaming through the pipeline.
    """
    consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'])

    consumer.assign([TopicPartition(topic=topic,partition=int(cam_num))])

    return Response(
        get_video_stream(consumer), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

def get_video_stream(consumer):
    """
    Here is where we recieve streamed images from the Kafka Server and convert 

    them to a Flask-readable format.
    """
    for msg in consumer:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + msg.value + b'\r\n\r\n')


# route to display stream of multiple cameras
@app.route("/cameras/<camera_numbers>")
def get_cameras(camera_numbers):
    return render_template("videos.html", cam_nums=list(range(int(camera_numbers))))


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000, debug=True)

