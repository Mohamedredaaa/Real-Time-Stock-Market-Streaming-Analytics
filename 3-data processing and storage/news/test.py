from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType
import joblib
import json
import re

# Load the pre-trained sentiment model and vectorizer
model = joblib.load('random_forest_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("KafkaSparkSentimentAnalysis") \
    .config("spark.sql.streaming.kafka.useDeprecatedOffsetFetching", "true") \
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2," 
            "com.datastax.spark:spark-cassandra-connector_2.12:3.0.0") \
    .getOrCreate()

# Set up Kafka source
kafka_brokers = 'localhost:9092'
kafka_topic = 'news_data'

# Read from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_brokers) \
    .option("subscribe", kafka_topic) \
    .load()

# Define schema for the incoming data
schema = "category STRING, datetime BIGINT, headline STRING, id INT, image STRING, related STRING, source STRING, summary STRING, url STRING"

# Convert the Kafka value column from bytes to JSON
df = df.selectExpr("CAST(value AS STRING)")

# Parse the JSON data
df = df.selectExpr("value as json").selectExpr("from_json(json, '{}') as data".format(schema)).select("data.*")

# Define sentiment mapping
sentiment_mapping = {
    0: "negative", 
    1: "neutral",  
    2: "positive"   
}

# Define a UDF for sentiment analysis
def predict_sentiment(summary):
    # Clean the text
    summary_cleaned = re.sub(r'[^\w\s]', '', summary.lower())  # Lowercase and remove punctuation
    summary_vectorized = vectorizer.transform([summary_cleaned])  # Vectorize the cleaned summary
    prediction = model.predict(summary_vectorized)  # Predict sentiment
    sentiment = sentiment_mapping.get(prediction[0], "unknown")  # Map numerical prediction to string
    return sentiment  # Return the sentiment string

# Register the UDF
sentiment_udf = udf(predict_sentiment, StringType())

# Apply the UDF to get the sentiment of the summary
df_with_sentiment = df.withColumn("sentiment", sentiment_udf(col("summary")))

# Select the desired columns including sentiment
df_selected = df_with_sentiment.select("summary", "sentiment")

# Set up a query to print the output to the console
query = df_selected.writeStream \
    .outputMode("append") \
    .format("console") \
    .start() 

# Wait for the termination of the query
query.awaitTermination()
