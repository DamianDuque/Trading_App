
## Agregar entradas
def add_row(filename, newRow):
    import csv
    #newRow = ["2023-08-13-13:00",1.374980,1.375270,1.372480,1.373100,60]
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(newRow)
    

## Editar valores
def edit_column(filename,columnNumber):
    import pandas as pd
    df = pd.read_csv(filename)
    actual = df.loc[columnNumber, 'operations']
    print(actual)
    modified = actual +1
    df.loc[0, 'operations'] = modified
    df.to_csv(filename, index=False)
  
    #print(df)

extraRow = ["2023-08-13-13:00",1.374980,1.375270,1.372480,1.373100,60]
add_row("test.csv", extraRow)
edit_column("test.csv", 0)


## Random numbers
import random
#periodPrices = []
average = 0

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

simulation(1,2,5)
average = round(average, 3)
#print(periodPrices)
print(average)