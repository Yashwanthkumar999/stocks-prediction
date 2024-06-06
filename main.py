import requests
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

API_key: str = "2N5I4DJ8QNXECMAE"

NEWS_API_KEY = "6ec11773fc1a4b3bab97e01d7c38e24a"

ACCOUNT_SID_TWILIO = "AC5682c9cbaa6c11f32402f92d38ebf8e6"
AUTH_TOKEN_TWILIO = "69980f5fbdf5f048e7b9361e0356417c"
TWILIO_PHONE_NO = "+18329253283"





STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_key
    }

response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETERS)

data = response.json()["Time Series (Daily)"]
my_list = [value for (key, value) in data.items()]
yesterdays_closing_price = my_list[0]["4. close"]
print(yesterdays_closing_price)


#TODO 2. - Get the day before yesterday's closing stock price

day_before_closing_price = my_list[1]["4. close"]
print(day_before_closing_price)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = (float(yesterdays_closing_price) - float(day_before_closing_price))
up_down = "None"
if difference >0:
    up_down = "📈"
else:
    up_down = "📉"


#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterdays_closing_price))*100)
print(diff_percent)


#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

NEWS_PARAMETERS = {
    "apikey": NEWS_API_KEY,
    "q": "TSLA",
}


response2 = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMETERS)
articles = response2.json()["articles"]





  ## STEP 2: https://newsapi.org/
  # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.


#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
top_3_articles = articles[:3]
formatted_articles = [f"{STOCK_NAME}:{up_down}{diff_percent}%\n Headline: {article['title']} \n Brief: {article['description']}" for article in top_3_articles]

if abs(diff_percent) > 1:

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

    #TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

    # CREATE twilio client account
    client = Client(ACCOUNT_SID_TWILIO, AUTH_TOKEN_TWILIO)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_PHONE_NO,
            to="+917075912537"
        )
    #TODO 9. - Send each article as a separate message via Twilio.



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

