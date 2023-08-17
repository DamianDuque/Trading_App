import os
import json
import pandas as pd
import plotly.graph_objects as go
from ManageFile import simulation

# function to add column with the average of the generated random numbers


def AddEdiCol(df):
    col = []
    df_max = df['High']
    df_min = df['Low']
    df_num = df['Number']

    for i in range(len(df_num)):
        col.append(simulation(df_min[i], df_max[i], df_num[i]))

    df["ValEd"] = col

    return df

# Function to make SMA line to a figure


def MakeTrace(df, refCol: str, color: str):
    return go.Scatter(x=df['Date'], y=df[refCol],
                      mode='lines', name=refCol, line_color=color)

# Function to calculate SMA to a DataFrame column


def CalcSMA(df, refCol: str, saveCol: str, sma: int):
    df[saveCol] = df[refCol].rolling(sma).mean()
    df[saveCol].fillna(df[refCol], inplace=True)

    return df


def jsonToDf(path):
    column_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Number']

    f = open(path)

    data = json.load(f)

    df = pd.DataFrame(list(zip(data['time'], data['open'], data['high'],
                      data['low'], data['close'], data['volume'])),
                      columns=column_names)

    df['Date'] = pd.to_datetime(df['Date'],
                                unit='s', origin='2000-1-1')
    return df


# jsonToDf("data/USA30IDXUSD_D1.json")


def csvToDf(path):
    column_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Number']
    return pd.read_csv(path, names=column_names)

# Function to create chart with data


def fileToChart(path: str, fmt: str):

    try:
        if fmt == "CSV":
            df = csvToDf(path)
        elif fmt == "JSON":
            df = jsonToDf(path)
    except Exception as ex:
        print(ex)
        return

    print("Processing image...")
    _, img_name = os.path.split(path)
    img_name = img_name.split('.')[0]
    img_path = 'img/{}.png' .format(img_name)
    df = AddEdiCol(df)
    df = CalcSMA(df, 'Close', 'SMA-5', 5)
    df = CalcSMA(df, 'Close', 'SMA-13', 13)
    df = CalcSMA(df, 'ValEd', 'SMA-E', 5)

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'],
                                         name="Candlestick")])

    sma_trace = MakeTrace(df, 'SMA-5', 'blue')
    sma_trace_2 = MakeTrace(df, 'SMA-13', 'purple')
    sma_trace_3 = MakeTrace(df, 'SMA-E', 'gray')

    fig.add_trace(sma_trace)
    fig.add_trace(sma_trace_2)
    fig.add_trace(sma_trace_3)
    fig.update_layout(
        title=dict(text=img_name, font=dict(size=30)),
        xaxis_rangeslider_visible=False
    )

    fig.write_image(img_path)

    return img_path


def test():
    path = input("Path: ")
    fileToChart(path)
