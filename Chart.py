import plotly.graph_objects as go
import pandas as pd
from ManageFile import simulation
import os


def AddEdiCol(df):
    col = []
    df_max = df['High']
    df_min = df['Low']
    df_num = df['Number']

    for i in range(len(df_num)):
        col.append(simulation(df_min[i], df_max[i], df_num[i]))

    df["ValEd"] = col

    return df


def CsvToChart(path: str, sma: int):
    column_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Number']

    try:
        df = pd.read_csv(path, names=column_names)
    except ValueError as er:
        print(er)
        return

    df = AddEdiCol(df)

    df['SMA'] = df['Close'].rolling(sma).mean()

    df['SMAE'] = df['ValEd'].rolling(sma).mean()

    df['SMA'].fillna(df['Close'], inplace=True)

    df['SMAE'].fillna(df['ValEd'], inplace=True)

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])

    sma_trace = go.Scatter(x=df['Date'], y=df['SMA'],
                           mode='lines', name='SMA', line_color=' blue')

    sma_trace_2 = go.Scatter(x=df['Date'], y=df['SMAE'],
                             mode='lines', name='SMAE', line_color='purple')

    fig.add_trace(sma_trace)
    fig.add_trace(sma_trace_2)

    img_path = 'img/{}.png' .format(os.path.splitext(path)[0])
    fig.write_image(img_path)
