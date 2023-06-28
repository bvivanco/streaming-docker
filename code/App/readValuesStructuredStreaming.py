#import sys
#from operator import add

from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

if __name__ == "__main__":
    spark = SparkSession\
            .builder \
            .appName("Streaming")\
            .master("local[3]")\
            .config("spark.streaming.stopGracefullyOnShutdown", "true")\
            .config("spark.sql.shuffle.partitions", 3)\
            .getOrCreate()
 

    linesDf = spark.readStream \
            .format("socket")\
            .option("host", "localhost")\
            .option("port", "9999")\
            .load()

    wordDf = linesDf.select(expr("explode(split(value,' ')) as word"))
    countsDf = wordDf.groupBy("word").count()

    wordCountQuery = countsDf.writeStream\
            .format("console")\
            .option("checkpointLocation", "chk-point-dir-2")\
            .outputMode("append")\
            .start()
    
    wordCountQuery.awaitTermination()
    