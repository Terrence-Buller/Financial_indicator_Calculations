import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

password = quote_plus("***")
engine = create_engine(f"mysql+mysqlconnector://***:{password}@localhost:***/crypto_data")
query = "SELECT * FROM btc_prices WHERE Date BETWEEN '2023-01-01' AND '2023-06-07' ORDER BY Date ASC"
df = pd.read_sql(query, engine)

# Chosen ema periods #
EMA_period = [10, 20, 50 ,100 ,200]

# for options in EMA_peiod calculate the k_value, takes the first value of the close column. 
# calculates the ema for all values in the number frame after [0], adds it to data frame of ema_values with the names of the ema_period EMA20 for example
for n in EMA_period:
    k = 2 / (n + 1)
    ema_values = [df['Close'][0]]
    for i in range(1, len(df)):
        ema = df['Close'][i] * k + ema_values[-1] * (1 - k)
        ema_values.append(ema)
    df[f'EMA{n}'] = ema_values

# for ammount of periods in EMA_periods repeat #
ema_columns = [f'EMA{n}' for n in EMA_period]

#multiple lines close + chosen ema_periods
y_axis = ['Close'] + ema_columns

fig1 = px.line(df, x='Date', y=y_axis, title='Average')
# thickening the line of Close #
fig1.update_traces(line=dict(width=4), selector=dict(name='Close'))
fig1.update_layout(template='presentation')
fig1.show()
