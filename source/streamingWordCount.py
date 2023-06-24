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
    
    #logger = Log4j(spark)

    linesDf = spark.readStream \
            .format("socket")\
            .option("host", "localhost")\
            .option("port", "9991")\
            .load()
    
    #linesDf.printSchema()

    #linesDf.show()

    wordDf = linesDf.select(expr("explode(split(value,' ')) as word"))
    countsDf = wordDf.groupBy("word").count()

    wordCountQuery = countsDf.writeStream\
            .format("console")\
            .option("checkpointLocation", "chk-point-dir")\
            .outputMode("complete")\
            .start()
    
    wordCountQuery.awaitTermination()
    