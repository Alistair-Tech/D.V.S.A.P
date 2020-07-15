
# Distributed-Video-Stream-Analytics-Platform (DVSAP)
In this project, we are streaming multiple videos using apache kafka and python. Also, we are using mongodb to store urls in our database and pymongo to access urls from database.

## Downloading and Installing mongodb
* Go to http://www.mongodb.org, then download and install MongoDB as per the instructions given there.
* Create a folder named mongodb on your computer and create a subfolder under it named data.
* Move to the mongodb folder and then start the MongoDB server by typing the following at the prompt:
```
 mongod --dbpath=data --bind_ip 127.0.0.1
```
* Open another command window and then type the following at the command prompt to start the mongo REPL shell:
```
mongo
```
* The Mongo REPL shell will start running and give you a prompt to issue commands to the MongoDB server. At the Mongo REPL prompt, type the following commands one by one and see the resulting behavior:
```
db
use video
db.user.insert({"key":"value"})
```
* Here I created a database named video,Inside that I am making a collection named user and then we can insert key-value pair inside the collection. In this example ,we will use key = "url" and and value is link.=======
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

Finally, make kafka topic with required number of partitions. For example,we want to stream 2 videos and our topic is video, then run this command:
```bash
# ./bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 2 --topic video
```
## Installing dependencies using pipenv
* In order to install all the dependecies for our project, go to terminal at location of the project and type:
```
pip install
```
* This will install all the required dependencies in your pip enviroment.
* In order to enter pip interactive shell, type:
```
pipenv shell
```

## Running the project
As you are now in pipenv shell, let us first execute our python code. Before running code, make sure your kafka and zookeeper is up and running and you have properly executed docker-compose file.
Running producer file:
```
pipenv run python producer.py
```
Now, as our producer file is running.
Running consumer file:
```
pipenv run python consumer.py
```

## Getting Results
In the shell, you will get a link.
To view our streams, we can do that in 2 ways.
1. **Different streams in different window**: For n streams, open n tabs in browser and in each tab, put url as -> link/cam/1, link/cam/2 .... upto link/cam/n.
2. **Different streams in single window**: For n streams, open a tab in browser and give it url as -> link/cameras/n
=======
Finally, start your kafka server by this command
```bash
#sudo  bin/kafka-server-start.sh config/server.properties
```

## Installing dependencies using pipenv
To install all the dependencies involved, we first need to install pipenv by using pip.
```bash
pip install pipenv
```
The Pipfile contains all the dependencies and to install them, we need to change to project directory and run the following command:
```bash
cd [Project Directory]
pipenv install
```
The above command actually creates a virtual environment in which all the dependencies are installed.
Now to run the python codes, you need to enter the virtual environemnt using the following command:
```bash
pipenv shell
```
We now can run the below python codes in this environment. 

If you would like to exit the environment at any moment, type exit.
```bash
exit
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

