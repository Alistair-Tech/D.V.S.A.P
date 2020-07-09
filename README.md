# Distributed Video streaming using kafka and python
Simple project to stream video using kafka and python. Check this [link](https://medium.com/@kevin.michael.horan/distributed-video-streaming-with-python-and-kafka-551de69fe1dd) for more details.

## Installing Docker and Docker compose
If you want to run your kafka and zookeeper on docker, follow these steps to set up docker in your system. [Reference](http://selftuts.com/kafaka-setup-using-docker-compose/). After you install docker and docker compose, you need to make a docker compose file (docker_compose.yml).

Now, to run kafka and zookeeper on your system, open terminal and follow these commands:

```bash
docker-compose -f docker-compose.yml up
```
This will start your kafka and zookeeper. Now, as your kafka and zookeeper is up and running, you can execute .yml file to interact with your kafka.
```bash
sudo docker exec -it kafka /bin/sh
```
Now, you are inside docker terminal, go to /opt/kafka
```bash
#cd /opt/Kafka/kafka_2.11-1.0.1/
```
Finally, start your kafka server by this command
```bash
#sudo  bin/kafka-server-start.sh config/server.properties
```

## Requirements 
To get our Kafka clients up and running, we’ll need the Kafka-Python installed on our system.
And, while we’re at it, we’ll also need OpenCV for video rendering, as well as Flask for our “distributed” Consumer.
To install these three, run the following command.
```bash
pip install kafka-python opencv-contrib-python Flask
```

## Python Code
Now everything is set up from kafka and you can now move on to our python code.

### Producer File
The first of our Kafka clients will be the message Producer. Here it will be responsible for converting video to a stream of JPEG images.
As you can see, the Producer defaults by streaming video directly from the web cam — assuming you have one. If pulling from a video file is more your style, the Producer accepts a file name as a command-line argument.

### Consumer File
To read our newly published stream, we’ll need a Consumer that accesses our Kafka topic. Since our message streamer was intended for a distributed system, we’ll keep our project in that spirit and launch our Consumer as a Flask service.


## Running the project
First start consumer file by opening new terminal and entering this command.
```bash
env FLASK_ENV=development FLASK_APP=consumer.py flask run
```
We are using this command so that our code runs in flask development enviroment.
After running this, we will get a link in the terminal. In the browser, go to link/video . You won’t see anything here yet, but keep it open cuz it’s about to come to life.

After this we can run producer code with RTSP link as argument.

```bash
python3 producer.py rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov
```
Then when we refresh the link, we will see our video being streamed in the browser. If you don't pass any arguments, then it will automatically get access to your webcam and stream the video.
