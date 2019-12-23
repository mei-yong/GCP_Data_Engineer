
# Example PySpark job

from pyspark.sql import SparkSession
from operator import add
import re

print("Okay Google.")

# Initialise a Spark pipeline
spark = SparkSession\
        .builder\
        .appName("CountUniqueWords")\
        .getOrCreate()

# Import the data & separate into lines
lines = spark.read.text("/sampledata/road-not-taken.txt").rdd.map(lambda x: x[0])

# Build the transformation pipeline - these are transforms and are not actually executed until the final action...
counts = lines.flatMap(lambda x: x.split(' ')) \
                  .filter(lambda x: re.sub('[^a-zA-Z]+', '', x)) \
                  .filter(lambda x: len(x)>1 ) \
                  .map(lambda x: x.upper()) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add) \
                  .sortByKey()
				  
# The final action which is collect in this case then executes the pipeline above
output = counts.collect()
for (word, count) in output:
  print("%s = %i" % (word, count))

spark.stop()


# The same PySpark job but outputs to a GS bucket

from pyspark.sql import SparkSession
from operator import add
import re

print("Okay Google.")

# Initialise a Spark pipeline
spark = SparkSession\
        .builder\
        .appName("CountUniqueWords")\
        .getOrCreate()

# Import the data & separate into lines
#lines = spark.read.text("/sampledata/road-not-taken.txt").rdd.map(lambda x: x[0])
lines = spark.read.text("gs://<YOUR-BUCKET>/road-not-taken.txt").rdd.map(lambda x: x[0])

# Build the transformation pipeline - these are transforms and are not actually executed until the final action...
counts = lines.flatMap(lambda x: x.split(' ')) \
                  .filter(lambda x: re.sub('[^a-zA-Z]+', '', x)) \
                  .filter(lambda x: len(x)>1 ) \
                  .map(lambda x: x.upper()) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add) \
                  .sortByKey()
				  
# The final action which is collect in this case then executes the pipeline above
output = counts.collect()
for (word, count) in output:
  print("%s = %i" % (word, count))

spark.stop()


