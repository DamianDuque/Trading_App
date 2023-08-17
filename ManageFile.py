# Agregar entradas
import csv
import pandas as pd
from datetime import datetime
import random

REQCOMMAND = ["REQ", "-p", "<PERIOD>", "-f",
              "<FORMAT(CSV,JSON)>", "-m", "<PAR>"]
#print(REQCOMMAND)
colum_names = ["Date", "Open", "High", "Low", "Close", "Number"]

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


def findPeriod(filename, columnNumber):
    stringFormat = "%Y-%m-%d %H:%M"
    validperiods = periods.keys()
    validResults = periods.values()
    validperiodsList = list(validperiods)
    validResultsList = list(validResults)

    df = pd.read_csv(filename, names=colum_names)
    date1 = df.loc[columnNumber, 'Date']
    date2 = df.loc[columnNumber+1, 'Date']
    date1_obj = datetime.strptime(date1, stringFormat)
    date2_obj = datetime.strptime(date2, stringFormat)
    difference = date2_obj-date1_obj
    backtostr = str(difference)
    if backtostr in validResultsList:
        position = validResultsList.index(backtostr)
        filePeriod = validperiodsList[position]
    else:
        filePeriod = "Invalid period"
        print(filePeriod)
        exit()

    return filePeriod


def findConversionRate(conversion):
    ratesKeys = conversionRates.keys()
    ratesValues = conversionRates.values()
    ratesKeysList = list(ratesKeys)
    ratesValuesList = list(ratesValues)
    print(ratesKeysList)
    print(ratesValuesList)

    if conversion in ratesKeysList:
        position = ratesKeysList.index(conversion)
        conversionRate = ratesValuesList[position]

        return conversionRate




def scaleFile(REQCOMMAND, filename, columnNumber):
    with open("newFile.csv", 'w') as f:
        print("New file created")

    if REQCOMMAND[1] == "-p":
        timePeriod = REQCOMMAND[2]
    else:
        timePeriod = "H1"

    df = pd.read_csv(filename, names=colum_names)  # Archivo original
    print(df)
    # test = len(df.index)
    # print(test)

    filePeriod = findPeriod(filename, columnNumber)
    # print(filePeriod)
    conversion = filePeriod + "-" + timePeriod
    # print(conversion)

    conversionRate = findConversionRate(conversion)
    # print(conversionRate)

    i = 0

    newrow = [0, 0, 0, 0, 0, 0]
    counter = 0
    while i < len(df.index):
        currentRow = df.loc[i]
        if counter == 0:
            newrow[0] = currentRow.Date
            newrow[1] = currentRow.Open
            newrow[2] = currentRow.High
            newrow[3] = currentRow.Low
            newrow[5] = 0

        if currentRow.High > newrow[2]:
            newrow[2] = currentRow.High

        if currentRow.Low < newrow[3]:
            newrow[2] = currentRow.Low

        newrow[4] = currentRow.Close

        newrow[5] = newrow[5] + currentRow.Number

        print(currentRow)
        print(newrow)
        i += 1
        print(i)
        counter += 1

        if counter == conversionRate or i == len(df.index):
            with open("newFile.csv", 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(newrow)
                counter = 0


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

# scaleFile([1,1,1,1,1],"data.csv",0)
