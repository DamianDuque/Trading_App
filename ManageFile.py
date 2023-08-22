# Agregar entradas
import csv
import pandas as pd
from datetime import datetime
import random
import os

colum_names = ["Date", "Open", "High", "Low", "Close", "Number"]
ruta = os.path.abspath("data")
newRow = [0,0,0,0,0,0]

periods = {
    "M1": "0:01:00",
    "M5": "0:05:00",
    "M15": "0:15:00",
    "M30": "0:30:00",
    "H1": "1:00:00",
    "H4": "4:00:00",
    "D1": "1 day, 0:00:00",
}

def findLine(days, seconds, i):
    if days >=1: 
        sameLine = False
    else:
        if seconds >= 60 and i == 0:
            sameLine = False
        elif seconds >= 300 and i == 1:
            sameLine = False
        elif seconds >= 900 and i == 2:
            sameLine = False
        elif seconds >= 1800 and i == 3:
            sameLine = False
        elif seconds >= 3600 and i == 4:
            sameLine = False
        elif seconds >= 14400 and i == 5:
            sameLine = False
        elif seconds >= 3600 and i == 4:
            sameLine = False
        elif seconds >= 86400 and i == 4:
            sameLine = False
        else:
            sameLine = True

    return sameLine

def sameRow(df, operationType, priceUpdate, filenames, validperiodsList, i):
    currentRow = df.loc[len(df.index)-1]
    newRow[0] = currentRow[0]
    newRow[1] = currentRow[1]
    price = currentRow[4]

    if operationType == "BUY":
        newRow[4] = float(currentRow[4]) * priceUpdate
        newRow[4] = round(newRow[4],3)
        if newRow[4] > float(currentRow[2]):
            newRow[2] = newRow[4]
            newRow[3] = currentRow[3]
        else:
            newRow[2] = currentRow[2]
            newRow[3] = currentRow[3]
    else: 
        newRow[4] = float(currentRow[4]) / priceUpdate
        newRow[4] = round(newRow[4],3)
        if newRow[4] < float(currentRow[3]):
            newRow[2] = currentRow[2]
            newRow[3] = newRow[4]
        else:
            newRow[2] = currentRow[2]
            newRow[3] = currentRow[3]

    newRow[5] = int(currentRow[5]) + 1
    print(newRow)
    df.iloc[-1] = newRow
    df = df.drop_duplicates()
    df = df.drop(0)
    print(df)
    print(priceUpdate)
    df.iloc[-1] = newRow
    newPrice = newRow[4]
    df.to_csv(os.path.join(ruta, filenames + "_" +validperiodsList[i]+ ".csv"), index=False)

    return price, newPrice

def diffRow(df, operationType, dt_string, priceUpdate, filenames, validperiodsList, i):
    currentRow = df.loc[len(df.index)-1]
    newRow[0] = dt_string
    newRow[1] = currentRow[4]
    price = currentRow[4]

    if operationType == "BUY":
        newRow[2] = float(currentRow[4]) * priceUpdate
        newRow[2] = round(float(newRow[2]),3)
        newRow[3] = newRow[1]
        newRow[4] = newRow[2]
    else: 
        newRow[2] = newRow[1]
        newRow[3] = float(newRow[1]) / priceUpdate
        newRow[3] = round(float(newRow[3]),3)
        newRow[4] = newRow[3]

    newRow[5] = 1
    newPrice = newRow[4]
    print(df)
    print(priceUpdate)
    with open(os.path.join(ruta, filenames + "_" + validperiodsList[i] + ".csv"), 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(newRow)

    return price, newPrice

def editCSV(filenames, operationType):
    priceUpdate = random.uniform(1,1.15)
    validperiods = periods.keys()
    validperiodsList = list(validperiods)
    i = 0
    while i < 7:
        df = pd.read_csv(os.path.join(ruta, filenames + "_" +validperiodsList[i]+ ".csv"), names=colum_names)
        stringFormat = "%Y-%m-%d %H:%M"
        date1 = df.loc[len(df.index)-1, 'Date']
        date1_obj = datetime.strptime(date1, stringFormat)
        date2 = datetime.now()
        dt_string = date2.strftime("%Y-%m-%d %H:%M")

        time_passed = date2 - date1_obj
        days = time_passed.days
        seconds = time_passed.seconds
        sameLine = findLine(days, seconds, i)

        if sameLine == True:
            price, newPrice = sameRow(df, operationType, priceUpdate, filenames, validperiodsList, i)
            

        else:
            price, newPrice = diffRow(df, operationType, dt_string, priceUpdate, filenames, validperiodsList, i)
            
        i=i+1

    return price, newPrice

def simulation(min, max, operations):
    average = 0
    i = 0
    count = 0
    while i < int(operations)-2:
        price = random.uniform(float(min), float(max))
        count = count + price
        i += 1
    average = count/(operations-2)
    return average
