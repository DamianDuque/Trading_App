from datetime import datetime
def scaleFile(filename, columnNumber):
    stringFormat = "%d-%m-%Y %H:%M"
    import pandas as pd
    df = pd.read_csv(filename)
    actual1 = df.loc[columnNumber, 'date']
    actual2 = df.loc[columnNumber+1, 'date']
    print(actual1)
    print(actual2)
    print(type(actual1))
    print(type(actual2))
    actualDate1 = datetime.strptime(actual1, stringFormat)
    actualDate2 = datetime.strptime(actual2, stringFormat)
    print(actualDate1)
    print(type(actualDate1))
    print(actualDate2)
    print(type(actualDate2))
    difference = actualDate2-actualDate1
    print(difference)
    backtostr = str(difference)
    print(backtostr)
    print(type(backtostr))
    #modified = actual + 1
    #df.loc[0, 'operations'] = modified
    #df.to_csv(filename, index=False)

    #print(df)

scaleFile("data.csv",0)
