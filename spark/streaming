from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType

spark = SparkSession.builder.appName("flowtrack_streaming").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("order_id", IntegerType()) \
    .add("customer_id", IntegerType()) \
    .add("event_time", StringType()) \
    .add("event_type", StringType()) \
    .add("delivery_status", StringType()) \
    .add("shipping_mode", StringType()) \
    .add("order_region", StringType()) \
    .add("order_country", StringType()) \
    .add("days_for_shipping_real", IntegerType()) \
    .add("days_for_shipment_scheduled", IntegerType()) \
    .add("late_delivery_risk", IntegerType())

raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "shipment_events") \
    .option("startingOffsets", "earliest") \
    .load()

parsed_df = raw_df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*")

query = parsed_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
