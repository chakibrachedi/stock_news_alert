import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "KP966V0BLX2HR9RE"
}
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_PARAMS = {
    "qInTitle": COMPANY_NAME,
    "apiKey": "55d243973965436ba83c1fd9ca3306df",
    "pageSize": 3,
    "language": "en"
}

stock_req = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMS)
stock_data = stock_req.json()['Time Series (Daily)']
stock_list = [value for (key, value) in stock_data.items()]

y_close = float(stock_list[0]["4. close"])
by_close = float(stock_list[1]["4. close"])
close_diff = y_close - by_close
diff_perc = round((close_diff / y_close) * 100)

up_down = None
if close_diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if abs(diff_perc) >= 0:
    news_req = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMS)
    news_data = news_req.json()['articles']
    formatted_articles = [f"{STOCK}: {up_down}{diff_perc}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in news_data]

    #TWILIO
    SID = "AC5c8c0da03a5513cc16812ada715d709b"
    TOKEN = "4c5f0bcafe332279c2d3edc8d9d32ca8"
    NUM = "+17603136943"
    client = Client(SID, TOKEN)
    for article in formatted_articles:
        msg = client.messages.create(body=article, from_=NUM, to="+213696390504")