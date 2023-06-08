import plotly.express as px
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host="***",
    user="***",
    password="***",
    database="***"
)

query = "SELECT * FROM btc_prices WHERE Date BETWEEN '2023-01-01' AND '2023-06-07' ORDER BY Date ASC"
df = pd.read_sql(query, mydb)

# data #
period = 14
change_values = [0]
avg_gain = [0] * 13
avg_loss = [0] * 13
RS = [0] * 13
RSI = [0] * 13


df['Change'] = df['Close'].pct_change()

df['Gain'] = df['Change'].apply(lambda x: x if x > 0 else 0)  # Making sure Negative numbers are reported as 0
df['Loss'] = df['Change'].apply(lambda x: x if x < 0 else 0)  # Making sure Postitive numbers get reported as 0

first_avg_gain = sum(df['Gain'][1:14]) / 14  # first average gain after 2 weeks #
first_avg_loss = sum(df['Loss'][1:14]) / 14  # first average losster 2 weeks #

avg_gain.append(first_avg_gain)
avg_loss.append(first_avg_loss)

for i in range(14, len(df)):
    prev_avg_gain = avg_gain[i - 1] # Takes the previous avg_gain for calculations #
    prev_avg_loss = avg_loss[i - 1] # Takes the previous avg_loss for calculations #
    curr_gain = df['Gain'][i]
    curr_loss = df['Loss'][i]
    new_avg_gain = ((prev_avg_gain * 13) + curr_gain) / 14  
    new_avg_loss = ((prev_avg_loss * 13) + curr_loss) / 14  
    avg_gain.append(new_avg_gain)
    avg_loss.append(new_avg_loss)

df['Avg_gain'] = avg_gain
df['Avg_loss'] = avg_loss

df['RS'] = df['Avg_gain'] / df['Avg_loss'].abs() # abs. to remove - #

for i in range(13, len(df)):
    rsi = 100 - (100 / (1 + df['RS'][i]))
    RSI.append(rsi)
df['RSI'] = RSI
df_filtered = df[13:] # only using data after day 13 #

for val in df_filtered['RSI']:
    if val <= 10:
        colors.append('#45B6FE')
    elif val <= 30:
        colors.append('green')
    elif val <= 70:
        colors.append('yellow')
    elif val <= 90:
        colors.append('red')
    else:
        colors.append('#000000')

custom_colors = [[0.0, '#45B6fe'],
                [0.35, '#00FF00'],
                [0.5, '#FFFF00'],
                [0.75, '#FF0000'],
                [0.95, '#000000'],
                [1.0, '#000000']]


fig = px.line(df_filtered, x='Date', y='RSI', title='RSI', markers=True, template='plotly_dark')

# Start after 14 days and capping it to 100 RSI max on the graph #
fig.update_layout(title='RSI', xaxis_range=['2023-01-14', df['Date'].max()], yaxis_range=[0, 100])

fig.update_traces(marker=dict(color=colors), line_color='white')
# heat map on the side #
fig.add_trace(go.Heatmap(z=[list(range(len(df_filtered)))], colorscale=custom_colors, showscale=True, zmin=0, zmax=100))


# Oversold line#
fig.add_hline(y=30, line_width=2, line_dash="dash", line_color="green")
#oversold text#
fig.add_annotation(
    xref='paper', yref='y',
    x=1.02, y=31,
    text='Oversold', showarrow=False,
    font=dict(color='green'), align='right'
)

# Overbought line#
fig.add_hline(y=70, line_width=2, line_dash="dash", line_color="red")
# Overbought text#
fig.add_annotation(
    xref='paper', yref='y',
    x=1.02, y=71,
    text='Overbought', showarrow=False,
    font=dict(color='red'), align='right'
)


fig.show()
                 
