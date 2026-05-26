from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = SparkSession.builder \
    .appName("KafkaToMinioFinal") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio-service:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "admin123") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "parques-vaga") \
    .option("startingOffsets", "earliest") \
    .load()

schema = StructType([
    StructField("id", StringType(), True),
    StructField("nome", StringType(), True),
    StructField("vagas", IntegerType(), True)
])

df_json = df.selectExpr("CAST(value AS STRING) as payload") \
    .select(from_json(col("payload"), schema).alias("data")) \
    .select("data.*")

query = df_json.writeStream \
    .format("parquet") \
    .option("path", "s3a://processed/streaming_data/") \
    .option("checkpointLocation", "/tmp/spark_checkpoint_final") \
    .start()

query.awaitTermination()