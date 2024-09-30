from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode, round, avg, count, sum
from pyspark.sql.types import StructType, StructField, DoubleType, LongType, StringType, ArrayType
from pyspark.sql import functions as F

# Initialize Spark session with Kafka and Cassandra support
spark = SparkSession.builder \
    .appName("Real-Time Stock Data Processing with Cassandra") \
    .config("spark.sql.streaming.kafka.useDeprecatedOffsetFetching", "true") \
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0") \
    .config("spark.cassandra.connection.host", "127.0.0.1") \
    .getOrCreate()

# Kafka setup
kafka_bootstrap_servers = "localhost:9092"  # Set your Kafka server
stock_topic = "stock_market_data"

# Define schema for stock data
stock_schema = StructType([
    StructField("data", ArrayType(StructType([
        StructField("c", ArrayType(StringType()), True),  # Column to drop
        StructField("p", DoubleType(), True),             # Price
        StructField("s", StringType(), True),             # Symbol
        StructField("t", LongType(), True),               # Timestamp
        StructField("v", DoubleType(), True)              # Volume
    ])), True),
    StructField("type", StringType(), True)
])

# Read stock data from Kafka
stock_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", stock_topic) \
    .option("startingOffsets", "latest") \
    .load() \
    .selectExpr("CAST(value AS STRING)").dropna() \
    .select(from_json("value", stock_schema).alias("data"))

# Explode the 'data' array and select individual fields, dropping the 'c' column
flattened_stock_stream = stock_stream \
    .select(explode(col("data.data")).alias("stock")) \
    .select(
        col("stock.p").alias("price"),      # Price
        col("stock.s").alias("symbol"),     # Symbol
        col("stock.t").alias("timestamp"),  # Timestamp
        col("stock.v").alias("volume")      # Volume
    )

# Cache to keep track of the last price for each stock symbol
# We are using a dictionary here to store the latest price of each stock symbol in memory.
last_prices = {}

# Function to alert if price change exceeds a certain percentage threshold
def check_price_alert(df):
    print("Processing...")  # This will print every time the function is called

    alert_threshold_percent = 5.0  # Define threshold for alert in percentage
    symbols_to_alert = []
    
    # Collect the data as rows
    alert_data = df.collect()
    
    for row in alert_data:
        symbol = row['symbol']
        current_price = row['price']
        
        # Check if we have seen this symbol before
        if symbol in last_prices:
            previous_price = last_prices[symbol]
            # Calculate percentage change
            price_change_percent = abs((current_price - previous_price) / previous_price) * 100
            
            if price_change_percent > alert_threshold_percent:
                symbols_to_alert.append({
                    'symbol': symbol,
                    'previous_price': previous_price,
                    'current_price': current_price,
                    'price_change_percent': price_change_percent,
                    'timestamp': row['timestamp']
                })
        
        # Update the last seen price
        last_prices[symbol] = current_price
    
    # Print alerts for the symbols that exceeded the threshold
    for alert in symbols_to_alert:
        print(f"ALERT: Stock {alert['symbol']} price changed by {alert['price_change_percent']:.2f}% "
              f"from {alert['previous_price']} to {alert['current_price']} at timestamp {alert['timestamp']}.")

# Write the cleaned stock data (with 'c' dropped) to Cassandra and alert if needed
def write_to_cassandra_main(df, epoch_id):
    check_price_alert(df)  # Call the alert function before writing to Cassandra
    df.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table="cleaned_stock_data", keyspace="stock_data_keyspace") \
        .save()

# Apply the cleaning and write operation to the main stock data
cleaned_stock_query = flattened_stock_stream \
    .writeStream \
    .foreachBatch(write_to_cassandra_main) \
    .outputMode("append") \
    .start()

# Group by 'symbol' and perform aggregations: average price, total volume, and count of trades
aggregated_stock_stream = flattened_stock_stream \
    .groupBy("symbol", "timestamp") \
    .agg(
        round(avg("price"), 2).alias("avg_price"),  # Average price rounded to 2 decimal places
        round(sum("volume"), 5).alias("total_volume"),  # Total volume rounded to 5 decimal places
        count("symbol").alias("trade_count")  # Count of trades
    )

# Write the aggregated data (analysis) to Cassandra
def write_to_cassandra_analysis(df, epoch_id):
    df.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table="stock_analysis", keyspace="stock_data_keyspace") \
        .save()

# Apply the write operation to the analysis data
analysis_stock_query = aggregated_stock_stream \
    .writeStream \
    .foreachBatch(write_to_cassandra_analysis) \
    .outputMode("update") \
    .start()

# Await termination to keep the stream alive
cleaned_stock_query.awaitTermination()
analysis_stock_query.awaitTermination()
