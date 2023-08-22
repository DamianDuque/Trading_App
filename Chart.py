import os
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.io import to_json
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


def jsonToDf(path, length):
    column_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Number']

    f = open(path)

    data = json.load(f)

    df = pd.DataFrame(list(zip(data['time'], data['open'], data['high'],
                      data['low'], data['close'], data['volume'])),
                      columns=column_names)

    df['Date'] = pd.to_datetime(df['Date'],
                                unit='s', origin='2000-1-1')
    return df.tail(length)


# jsonToDf("data/USA30IDXUSD_D1.json")


def csvToDf(path, length):
    column_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Number']
    df = pd.read_csv(path, names=column_names)

    return df.tail(length)

# Function to create chart with data


def fileToChart(path: str, fmt: str):
    data_length = 1000
    try:
        if fmt == "CSV":
            df = csvToDf(path, data_length)
        elif fmt == "JSON":
            df = jsonToDf(path, data_length)
    except Exception as ex:
        print(ex)
        return

    print("Processing image...")
    _, img_name = os.path.split(path)
    img_name = img_name.split('.')[0]
    img_path = 'img/{}.png' .format(img_name)
    # df = AddEdiCol(df)
    df = CalcSMA(df, 'Close', 'SMA-5', 5)
    df = CalcSMA(df, 'Close', 'SMA-13', 13)
    # df = CalcSMA(df, 'ValEd', 'SMA-E', 5)

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'],
                                         name="Candlestick")])

    sma_trace = MakeTrace(df, 'SMA-5', 'blue')
    sma_trace_2 = MakeTrace(df, 'SMA-13', 'purple')
    # sma_trace_3 = MakeTrace(df, 'SMA-E', 'gray')

    fig.add_trace(sma_trace)
    fig.add_trace(sma_trace_2)
    # fig.add_trace(sma_trace_3)

    fig.write_image(img_path)

    graph = to_json(fig)

    return graph


def test():
    path = input("Path: ")
    fmt = input("Format: ")
    fileToChart(path, fmt)
