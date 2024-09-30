
# Real-Time Stock Market Analysis Using Streaming Processing

## Project Overview

This project, titled **Real-Time Stock Market Analysis Using Streaming Processing**, focuses on tracking live stock prices and performing sentiment analysis on related news articles. The key objective is to gain insights into market trends, volume, and price fluctuations in real time. Additionally, alerting mechanisms are incorporated to notify users based on threshold conditions such as price drops.

The project utilizes various big data technologies for data ingestion, processing, storage, and visualization.

---

## Table of Contents

1. [Technologies Used](#technologies-used)
2. [Project Components](#project-components)
   - [Stock Data Ingestion](#stock-data-ingestion)
   - [News Data Ingestion](#news-data-ingestion)
   - [Real-Time Processing](#real-time-processing)
   - [Data Storage](#data-storage)
   - [Data Visualization](#data-visualization)
3. [System Setup](#system-setup)
   - [Environment Configuration](#environment-configuration)
4. [Running the Project](#running-the-project)
5. [Results](#results)
6. [Future Improvements](#future-improvements)
7. [Contributors](#contributors)

---

## Technologies Used

- **Apache Kafka** for real-time data ingestion of stock and news data
- **Apache Flume** for ingesting news data
- **Apache Spark (PySpark)** for real-time stream processing
- **Cassandra** for data storage
- **MongoDB and Kibana** for data visualization and querying
- **Alpha Vantage API** for stock market data
- **Python** for sentiment analysis
- **Java 1.8** for compatibility with big data tools

---

## Project Components

### 1. Stock Data Ingestion

We used **Kafka** for ingesting real-time stock data. The stock data is fetched using the **Alpha Vantage API** and streamed into a Kafka topic named `stock-data-csv`. The stock data includes the following fields:
- `symbol`: Stock symbol
- `date`: Trading date
- `open`: Opening price
- `high`: Highest price
- `low`: Lowest price
- `close`: Closing price
- `volume`: Number of shares traded
- `close_usd`: Closing price in USD

### 2. News Data Ingestion

**Apache Flume** was configured to ingest live news articles related to stock markets. The pipeline was set up to monitor a directory (`spoolDir`) and transfer the logs to Kafka for further analysis. We used Flume agents to watch for new log files and transfer them in real time.

### 3. Real-Time Processing

We processed the ingested data using **Apache Spark Streaming**. The processing included:
- Calculation of the average price, total volume, and trade count.
- Aggregating stock data based on symbols.
- **Sentiment analysis** on the ingested news articles using natural language processing (NLP) libraries in Python.

### 4. Data Storage

We used **Cassandra** to store the processed stock data. The schema in Cassandra was designed as follows:
- Keyspace: `stock_data_ks`
- Table: `stock_data`
  - `symbol`
  - `avg_price`
  - `total_volume`
  - `trade_count`

The processed data from Spark was written to Cassandra for persistent storage.

### 5. Data Visualization

For querying and visualizing the stored data, we used **MongoDB** along with **Kibana**. The visualizations included:
- Real-time stock prices and trends.
- Volume analysis and trend identification.
- Alerts for specific conditions like price drops below a defined threshold.

---

## System Setup

### 1. Environment Configuration

The project was developed and deployed using the following setup:
- **Operating System**: CentOS 7 (running on a VM)
- **Java Version**: 1.8.0_291
- **Hadoop** for distributed storage
- **Apache Kafka** for stock data streaming (running at IP `192.168.109.129`)
- **Flume** for news ingestion
- **Cassandra** for database storage
- **Spark** for real-time processing
- **Jupyter Notebook** for running PySpark code
- **Kibana** for visualizing stock trends

### 2. Kafka Configuration

The Kafka topic `stock-data-csv` was used to stream stock data in real-time. Remote access and configuration were performed on the IP address `192.168.109.129`. The following steps were followed to configure Kafka:
- Kafka broker setup.
- Zookeeper configuration (client port: 2181).
- Remote connection configurations for external access.

### 3. Spark Setup

Spark was used for both batch and streaming data processing. The configuration included:
- Defining a schema for the incoming CSV data.
- Reading and processing stock data in real-time.
- Writing output to Cassandra.

---

## Running the Project

1. **Stock Data Ingestion**:
   - Start the Kafka broker and Zookeeper.
   - Run the Python script to fetch data from the Alpha Vantage API and stream it to Kafka.

2. **News Data Ingestion**:
   - Configure and start the Flume agent to monitor the log directory and transfer data to Kafka.

3. **Real-Time Processing**:
   - Run the Spark Streaming job to process the stock and news data.
   - Perform sentiment analysis on news articles.

4. **Data Storage and Visualization**:
   - Ensure Cassandra is running and available.
   - Spark writes processed data to Cassandra.
   - Use Kibana to visualize the stored data.

---

## Results

- **Real-time Price Analysis**: The system was able to successfully track real-time stock prices, allowing for in-depth market analysis.
- **Volume and Trend Monitoring**: The data on traded volume and stock price movements provided key insights into market trends.
- **Sentiment Analysis**: Sentiment analysis on the news articles was integrated to analyze the mood around specific stocks.
- **Alerts**: Alerts were triggered based on price drops or volume thresholds.

---

## Future Improvements

1. **Scalability**: Scaling the system to ingest more stock symbols and news articles in parallel.
2. **Machine Learning Integration**: Incorporating machine learning models for predictive analytics.
3. **Advanced Visualizations**: Adding more comprehensive and interactive visualizations in Kibana for better decision-making.

---

## Contributors

- **Mohamed Reda** - [LinkedIn](https://www.linkedin.com/in/mohamed-amer-2b5754190/)
- **Team Members**:
  - Abdelrahman Elmagry - [LinkedIn](https://www.linkedin.com/in/elmagry123)
  - Maya Assem - [LinkedIn](https://www.linkedin.com/in/maya-assem-611b4723b)
  - Nancy Youssef - [LinkedIn](https://www.linkedin.com/in/nancy-youssef-16649124a)
- **Instructors and Facilitators**:
  - Salma Khaled - [LinkedIn](https://www.linkedin.com/in/salma-khaled-8034a8203)
  - Sara Baza - [LinkedIn](https://www.linkedin.com/in/sara-baza-553b441b0)
  - Abdelrahman Mahmoud - [LinkedIn](https://www.linkedin.com/in/abdelrahman-mahmoud-9720221a7)
  - Ahmed Abdelnasser - [LinkedIn](https://www.linkedin.com/in/ahmed-abdelnasser-sayed)

