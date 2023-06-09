import requests
from twilio.rest import Client

STOCK = "TSLA" # you can change the initials for no matter what company you wish for
COMPANY_NAME = "Tesla Inc"

TWILIO_SID = "YOUR TWILIO SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

alphavantage_api_key = "ALPHA API KEY"
newsapikey = "NEWS API KEY"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOIT = "https://newsapi.org/v2/everything"

# Stock Data Request

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": alphavantage_api_key,
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_data = stock_response.json()["Time Series (Daily)"]
# transforming data dictionary into a list
stock_data_list = [value for (key, value) in stock_data.items()]
# recovering the data
day_before_yesterday_stock_data = stock_data_list[1]
yesterday_stock_data = stock_data_list[0]
# recovering the closing price
day_before_yesterday_closing_price = day_before_yesterday_stock_data["4. close"]
yesterday_stock_closing_price = yesterday_stock_data["4. close"]
# Difference
difference = float(yesterday_stock_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"
# comparing the price
diff_percent = round(difference / float(yesterday_stock_closing_price)) * 100

if abs(diff_percent) > 5:
    # News Data Request
    news_params = {
        "apiKey": newsapikey,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOIT, params=news_params)
    articles = news_response.json()["articles"]
    # keeps the first 3 articles
    first_three_articles = articles[:3]
    # makes a list with title and description
    formated_article_list = [
        f"{STOCK}:{up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article
        in
        first_three_articles]
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formated_article_list:
        message = client.messages.create(
            body=article,
            from_='YOUR TWILIO PHONE NUMBER',
            to="DESTINATION PHONE NUMBER",
        )
        print(message.status)
