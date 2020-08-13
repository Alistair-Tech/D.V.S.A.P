from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from multiprocessing import Process
import json
import time

# topic we read the frames from
topic = 'video'

# creating a spark session
spark = SparkSession \
    .builder \
    .appName('myapp') \
    .getOrCreate()

# connect to kafka topic partition to read the input frames and store the data in df_raw
df_raw = spark \
  .readStream \
  .format('kafka') \
  .option('kafka.bootstrap.servers', 'localhost:9092') \
  .option('assign',json.dumps({topic: [0]})) \
  .option('failOnDataLoss','false') \
  .load()

# the returned table has many columns like key, value, topic, partition, timestamp
# we need only value column
df_value = df_raw.selectExpr('value')

# just to check the schema
df_value.printSchema()


# function to apply our ML model
def apply_model(data):
  from model1 import detect
  return detect(data)
  # return data

# udf - User Defined Function to apply to each row of our table
model_udf = udf(apply_model,BinaryType())

# apply the model to all rows in df_value and store the processed frames in df_processed
df_processed = df_value.select(model_udf('value'))


# use the following code to write the processed frames to console
df_processed.toDF('value') \
               .writeStream \
               .format("console") \
               .start() \
               .awaitTermination()