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

## Setting up the database from which RTSP links will be queried
Before running the python codes, we will have to set up a database of RTSP links.


## Python Code
Now everything is set up from kafka and you can now move on to our python code.

### Producer File
The first of our Kafka clients will be the message Producer. Here it will be responsible for converting video to a stream of JPEG images.
As you can see, the Producer first queries the RTSP links stored in a database and stores it. 

We have a VideoStreaming producer process class that writes to a kafka topic the JPEG images converted to bytes from a given RTSP link. To facilitate simultaneous writing of different streams to kafka, we take advantage of partitions in a topic. 

We now start one process for each of the RTSP links and they write to their respective partitions simultaneously. 

### Consumer File
To read our newly published stream, we’ll need a Consumer that accesses our Kafka topic. Since our message streamer was intended for a distributed system, we’ll keep our project in that spirit and launch our Consumer as a Flask service. 

## Running the project
First start consumer file by opening new terminal and entering this command.
```bash
python consumer.py
```
After running this, we will get a [link] in the terminal. 

There are 2 types of routes in which streams can be viewed in browser.

The first route is as follows:
```bash
[link]/cam/[cam_num]
```
This route consumes the stream of a specific camera denoted by <cam_num>.

The second route is as follows:
```bash
[link]/cameras/[cam_nums]
```
This route consumes multiple streams and displays all of them in one page. The [cam_nums] denote the number of streams to be displayed in the page.

Note: Flask is unable to load more than 6 streams at once. It displays 'waiting for available socket' if more than 6 streams are called at once. We are working on it.

You won’t see anything here yet, but keep it open cuz it’s about to come to life.

After this we can run producer code with RTSP link as argument.

```bash
python producer.py
```
Then when we refresh the link, we will see our video(s) being streamed in the browser.
