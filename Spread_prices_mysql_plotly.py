import mysql.connector
import requests
from datetime import datetime
import time

currencies = ["BTC", "ETH", (etc.)]

mydb = mysql.connector.connect(
    host="***",
    user="***",
    password="***",
    database="***"
)

mycursor = mydb.cursor()

def getcoins(currencies):
    for i in range(24):  # run it 24 times
        for currency in currencies:

            ### connecting to the api and retrieving the data ###
            url = f"https://data.binance.com/api/v3/depth?limit=1&symbol={currency}USDT"
            response = requests.get(url)
            if response.status_code == 200:
                results = response.json()
                coin = f"{currency}"
                now = datetime.now()
                timestamp = now.strftime("%d/%m/%Y %H:%M:%S:%f")[:-3] # making sure MS only consists of 3 numbers day-month-year hour-minute-second-milisecond #
                all_data = []
                bids = results['bids']
                asks = results['asks']
                times = timestamp
                spread = [float(ask[0]) - float(bid[0]) for ask, bid in zip(asks, bids)] #add asks and bids (2, 1) subtract them for the spread ##
                bid_ask_percentage = [((float(ask[0]) - float(bid[0])) / float(ask[0])) * 100 for ask, bid in
                                      zip(asks, bids)]

                all_data.append({'Coin': coin,
                                 'Date_time': times,
                                 'Bid_price': [float(bid[0]) for bid in bids],  
                                 'Ask_price': [float(ask[0]) for ask in asks],
                                 'Spread': spread,
                                 'Spread_percentage': bid_ask_percentage
                                 })

                print(all_data)
                sql = "INSERT INTO spread (Coin, Date_time, Bid_price, Ask_price, Spread, Spread_percentage) VALUES (%s, " \
                      "%s, %s, %s, %s, %s)"
                values = (coin, times, results['bids'][0][0], results['asks'][0][0], spread[0], bid_ask_percentage[0])  # 1st[0] picks the first bid, 2nd[0] picks the first list price ([1] is quantity)
                mycursor.execute(sql, values)
            else:
                print("Error")



            mydb.commit()
        time.sleep(3600) # wait an hour #


getcoins(currencies)

### plotly part ###
query1 = "SELECT * from Spread"

df = pd.read_sql(query1, mydb)

fig = px.line(df, x='Date_time', y='Spread', title='Spread over Time', labels={'Date_time': 'Date and Time'}, template="plotly_dark")
fig.update_traces(line_color='#ffe28a', line_width=3)
fig.show()
