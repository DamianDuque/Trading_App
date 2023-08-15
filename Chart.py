import plotly.graph_objects as go
import pandas as pd
from ManageFile import simulation
import os

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

# Function to create chart with data


def CsvToChart(path: str):
    column_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Number']

    try:
        df = pd.read_csv(path, names=column_names)
    except Exception as ex:
        print(ex)
        return

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
        title=dict(text=img_name, font=dict(size=30))
    )

    fig.write_image(img_path)


def test():
    path = input("Path: ")
    CsvToChart(path)
