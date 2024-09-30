import requests
import json
import time

API_KEY = 'crlmpl1r01qnaav315cgcrlmpl1r01qnaav315d0'
API_URL = 'https://finnhub.io/api/v1/news?category=general&token=' + API_KEY

def fetch_news():
    response = requests.get(API_URL)
    data = response.json()
    return data

while True:
    news_data = fetch_news()
    for item in news_data:
        print(json.dumps(item))  # Print to console, Flume will read this
    time.sleep(50)  # Fetch data every 30 seconds

