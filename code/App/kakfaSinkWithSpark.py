#import sys
#from operator import add

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import pyspark.sql.functions as F


def promediarValores(df):
   df.createOrReplaceTempView("vResultado")
   promedios = spark.sql("""SELECT nombre, apellido, pais FROM vResultado""")
   return promedios




if __name__ == "__main__":
    spark = SparkSession\
            .builder \
            .appName("Streaming")\
            .master("local[3]")\
            .config("spark.streaming.stopGracefullyOnShutdown", "true")\
            .config("spark.sql.shuffle.partitions", 3)\
            .getOrCreate()
    
    
    tiposStreamingDF = (spark\
                        .readStream\
                        .format("kafka")\
                        .option("kafka.bootstrap.servers", "localhost:9092")\
                        .option("subscribe", "mensaje")\
                        .load())
    
    esquema = StructType([\
        StructField("nombre", StringType()),\
        StructField("apellido", StringType()),\
        StructField("pais", StringType())\
        ])
    
    parsedDF = tiposStreamingDF\
        .select("value")\
        .withColumn("value", F.col("value").cast(StringType()))\
        .withColumn("input", F.from_json(F.col("value"), esquema))\
        .withColumn("nombre", F.col("input.nombre"))\
        .withColumn("apellido", F.col("input.apellido"))\
        .withColumn("pais", F.col("input.pais"))

    promediosStreamingDF = promediarValores(parsedDF)
    
    salida = promediosStreamingDF\
        .writeStream\
        .queryName("AgregacionBaseContactos")\
        .outputMode("append")\
        .format("memory")\
        .start()
    
    spark.sql("select * from AgregacionBaseContactos").show
    
    salida.awaitTermination()
    