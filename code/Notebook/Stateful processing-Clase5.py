# Databricks notebook source
spark.conf.set("spark.sql.shuffle.partitions", 5)

# COMMAND ----------

# MAGIC %fs ls /FileStore/train-spark/data/activity-data

# COMMAND ----------

path = '/FileStore/train-spark/data/activity-data'
static = spark.read.json(path)
streaming = spark\
  .readStream\
  .schema(static.schema)\
  .option("maxFilesPerTrigger", 5)\
  .json(path)

# COMMAND ----------

countDf = static.count()
print(countDf)

# COMMAND ----------

display(static)

# COMMAND ----------

static.printSchema

# COMMAND ----------

withEventTime = streaming.selectExpr(
  "*",
  "cast(cast(Creation_Time as double)/1000000000 as timestamp) as event_time")

# COMMAND ----------

# MAGIC %md
# MAGIC ##Tumbling windows

# COMMAND ----------

from pyspark.sql.functions import window, col
eventTimeGroup = (withEventTime.groupBy(window(col("event_time"), "10 minutes"), withEventTime.Model).count()\
  .writeStream\
  .queryName("pyevents_per_window1")\
  .format("memory")\
  .outputMode("complete")\
  .start())

# COMMAND ----------

windowsDf1 = spark.sql("select * from pyevents_per_window1")
display(windowsDf1)
#windowsDf.show(100, False)

# COMMAND ----------

windowsDf.printSchema()

# COMMAND ----------

spark.sql("select count(*) AS num from pyevents_per_window").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ##Slicing Windows

# COMMAND ----------

from pyspark.sql.functions import window, col
withEventTime.groupBy(window(col("event_time"), "10 minutes", "5 minutes"))\
  .count()\
  .writeStream\
  .queryName("pyevents_per_window2")\
  .format("memory")\
  .outputMode("complete")\
  .start()

# COMMAND ----------

windowsDf2 = spark.sql("select * from pyevents_per_window2")
display(windowsDf)

# COMMAND ----------

# MAGIC %md
# MAGIC ##Watermarks

# COMMAND ----------

from pyspark.sql.functions import window, col
withEventTime\
  .withWatermark("event_time", "30 minutes")\
  .groupBy(window(col("event_time"), "10 minutes", "5 minutes"))\
  .count()\
  .writeStream\
  .queryName("pyevents_per_window3")\
  .format("memory")\
  .outputMode("complete")\
  .start()

# COMMAND ----------

#spark.sql("select * from pyevents_per_window3 ORDER BY window.start ASC").show(100, False)
spark.sql("select * from pyevents_per_window3").show(100, False)

# COMMAND ----------

# MAGIC %md
# MAGIC ##Deduplication

# COMMAND ----------

from pyspark.sql.functions import expr

withEventTime\
  .withWatermark("event_time", "5 seconds")\
  .dropDuplicates(["User", "event_time"])\
  .groupBy("User")\
  .count()\
  .writeStream\
  .queryName("pydeduplicated")\
  .format("memory")\
  .outputMode("complete")\
  .start()

# COMMAND ----------

spark.sql("select * from pydeduplicated").show(100, False)
