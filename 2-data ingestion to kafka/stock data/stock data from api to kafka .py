import websocket
import json
from kafka import KafkaProducer

# Kafka Producer configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092' 
KAFKA_TOPIC_STOCK_MARKET = 'stock_market_data'

# Finnhub API configuration
FINNHUB_API_TOKEN = 'cri7b39r01qqt33r9ar0cri7b39r01qqt33r9arg'
FINNHUB_API_URL = 'wss://ws.finnhub.io?token=' + FINNHUB_API_TOKEN

# Kafka Producer instance
producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

# Function to send data to Kafka
def send_to_kafka(topic, data):
    producer.send(topic, value=data.encode('utf-8'))
    print(f"Sent data to Kafka topic {topic}: {data}")

# Function to handle Finnhub API WebSocket messages
def on_message(ws, message):
    data = json.loads(message)
    send_to_kafka(KAFKA_TOPIC_STOCK_MARKET, json.dumps(data))

# WebSocket connection to Finnhub API
ws = websocket.WebSocketApp(FINNHUB_API_URL, on_message=on_message)
ws.on_open = lambda ws: [
    ws.send('{"type":"subscribe","symbol":"AAPL"}'),
    ws.send('{"type":"subscribe","symbol":"AMZN"}'),
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}'),
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}'),
    ws.send('{"type":"subscribe","symbol":"MSFT"}')
]

# Start the WebSocket connection
ws.run_forever()
