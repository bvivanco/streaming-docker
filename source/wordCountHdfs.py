import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

if __name__ == "__main__":
    print(sys.argv)
    print('vamos bien')
    print(f'el archivo es: {sys.argv[1]}')

    """
    if len(sys.argv) != 2:
        print("Usage: hdfs_wordcount.py <directory>", file=sys.stderr)
        sys.exit(-1)
    """

    sc = SparkContext(appName="StreamingStorage")
    ssc = StreamingContext(sc, 1)

    lines = ssc.textFileStream(sys.argv[1])

    """counts = lines.flatMap(lambda line: line.split(" "))\
                  .map(lambda x: (x, 1))\
                  .reduceByKey(lambda a, b: a + b)
    """
    counts = lines.flatMap(lambda line: line.split(" "))\
                .map(lambda x: (x,1))\
                .reduceByKey(lambda a,b: a + b)
    #counts.pprint()
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()