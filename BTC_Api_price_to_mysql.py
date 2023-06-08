import mysql.connector
import requests
from datetime import datetime
import pandas as pd
import time

mydb = mysql.connector.connect(
    host="***",
    user="***",
    password="***",
    database="***"
)

mycursor = mydb.cursor()

for i in range(10):
    all_data = []
    now = datetime.now()
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(url).json()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S:%f")[:-3] # 3 numbers for the MS #
    all_data.append({
        'symbol': data['symbol'],
        'price': data['price'],
        'time' : timestamp
        })

    df = pd.DataFrame(all_data)
    sql = "INSERT INTO prices (coin, price, time) VALUES (%s, %s, %s)"
    values = (data['symbol'], data['price'], timestamp)
    mycursor.execute(sql, values)
    mydb.commit()

time.sleep(86400) # wait a day #
