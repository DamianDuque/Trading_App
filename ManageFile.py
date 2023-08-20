# Agregar entradas
import csv
import pandas as pd
from datetime import datetime
import random
import os

REQCOMMAND = ["REQ", "-p", "<PERIOD>", "-f",
              "<FORMAT(CSV,JSON)>", "-m", "<PAR>"]
#print(REQCOMMAND)
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

conversionRates = {
    "M1-M1": 1, "M1-M5": 5, "M1-M15": 15, "M1-M30": 30, "M1-H1": 60, "M1-H4": 240, "M1-D1": 1440,
    "M5-M1": "Invalid", "M5-M5": 1, "M5-M15": 3, "M5-M30": 6, "M5-H1": 12, "M5-H4": 48, "M5-D1": 288,
    "M15-M1": "Invalid", "M15-M5": "Invalid", "M15-M15": 1, "M15-M30": 2, "M15-H1": 4, "M15-H4": 16, "M15-D1": 96,
    "M30-M1": "Invalid", "M30-M5": "Invalid", "M30-M15": "Invalid", "M30-M30": 1, "M30-H1": 2, "M30-H4": 8, "M30-D1": 48,
    "H1-M1": "Invalid", "H1-M5": "Invalid", "H1-M15": "Invalid", "H1-M30": "Invalid",  "H1-H1": 1, "H1-H4": 4, "H1-D1": 24,
    "H4-M1": "Invalid", "H4-M5": "Invalid", "H4-M15": "Invalid", "H4-M30": "Invalid", "H4-H1": "Invalid", "H4-H4": 1, "H4-D1": 6,
    "D1-M1": "Invalid", "D1-M5": "Invalid", "D1-M15": "Invalid", "D1-M30": "Invalid", "D1-H1": "Invalid", "D1-H4": "Invalid", "D1-D1": 1,
}


def editCSV(filenames, operationType):
    priceUpdate = 10
    validperiods = periods.keys()
    validperiodsList = list(validperiods)
    i = 0
    while i < 7:
        df = pd.read_csv(os.path.join(ruta, filenames + "_" +validperiodsList[i]+ ".csv"), names=colum_names)
        stringFormat = "%Y-%m-%d %H:%M"
        #print(df)
        date1 = df.loc[len(df.index)-1, 'Date']
        date1_obj = datetime.strptime(date1, stringFormat)
        date2 = datetime.now()
        dt_string = date2.strftime("%Y-%m-%d %H:%M")

        time_passed = date2 - date1_obj
        days = time_passed.days
        seconds = time_passed.seconds
        #print(days,seconds)
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

        if sameLine == True:
            currentRow = df.loc[len(df.index)-1]
            newRow[0] = currentRow[0]
            newRow[1] = currentRow[1]
            price = currentRow[4]

            if operationType == "BUY":
                newRow[4] = float(currentRow[4]) + priceUpdate
                if newRow[4] > float(currentRow[2]):
                    newRow[2] = newRow[4]
                    newRow[3] = currentRow[3]
                else:
                    newRow[2] = currentRow[2]
                    newRow[3] = currentRow[3]
            else: 
                newRow[4] = float(currentRow[4]) - priceUpdate
                if newRow[4] < float(currentRow[3]):
                    newRow[2] = newRow[2]
                    newRow[3] = newRow[4]
                else:
                    newRow[2] = currentRow[2]
                    newRow[3] = currentRow[3]

            newRow[5] = int(currentRow[5]) + 1
            print(newRow)
            #print(df)
            df.iloc[-1] = newRow
            df = df.drop_duplicates()
            df = df.drop(0)
            print(df)
            #print("Reformed df:")
            #print(df)
            #df.loc[df.shape[0]]  = newRow
            #print("Final df")
            #print(df)
            df.iloc[-1] = newRow
            #print(df)
            df.to_csv(os.path.join(ruta, filenames + "_" +validperiodsList[i]+ ".csv"), index=False)

            # with open(os.path.join(ruta, filenames + "_" +validperiodsList[i]+ ".csv"), 'a', newline='') as f:
            #     writer = csv.writer(f)
            #     writer.writerow(newRow)

        else:
            currentRow = df.loc[len(df.index)-1]
            #print(currentRow)
            newRow[0] = dt_string
            newRow[1] = currentRow[4]
            price = currentRow[4]

            if operationType == "BUY":
                newRow[2] = float(currentRow[4]) + priceUpdate
                newRow[3] = newRow[1]
                newRow[4] = newRow[2]
            else: 
                newRow[2] = newRow[1]
                newRow[3] = float(newRow[1]) - priceUpdate
                newRow[4] = newRow[3]

            newRow[5] = 1

            with open(os.path.join(ruta, filenames + "_" + validperiodsList[i] + ".csv"), 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(newRow)


        newPrice = newRow[4]
        #print("period ", i, "ready")
        #print(validperiodsList[i])
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


editCSV("BTCUSD", "SELL")