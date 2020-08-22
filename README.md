
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
* Here I created a database named video,Inside that I am making a collection named user and then we can insert key-value pair inside the collection. In this example ,we will use key = "url" and and value is link.


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

Finally, make kafka topic with required number of partitions. For example,if we want to stream 2 videos and our topic is video, then run this command:
```bash
# ./bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 2 --topic video
```

# Installing Spark
For setting up spark on your system, check out this site: [link](https://phoenixnap.com/kb/install-spark-on-ubuntu).


# Installing Dependencies

### Installing dependencies using pipenv for producer and consumer file
* In order to install all the dependecies for our project, go to terminal at location of the project and type:
```
pip install
```
* This will install all the required dependencies in your pip enviroment.
* In order to enter pip interactive shell, type:
```
pipenv shell
```
### Dependencies for spark file
As we have to run the spark file where we installed the spark module, install the dependencies mentioned in requirements.txt file.

## Running the project
First make a folder named static and insided that , make another folder named model1 to store the output images.
Now, Go to pipenv shell, let us first execute our python code. Before running code, make sure your kafka and zookeeper is up and running and you have properly executed docker-compose file.
Running producer file:
```
pipenv run python producer.py
```
Now, as our producer file is running.

Then run the spark.py file at its location.

Finally, run the consumer file in pipenv shell.
Running consumer file:
```
pipenv run python consumer.py
```

## Getting Results
In the shell where you are running consumer file, you will get a link.
To view the output, go to link/getViolations.
