
import os, csv, pretty_errors
import pandas as pd

for f in os.scandir():
    if ".csv" in f.name:
        filename = f.name

data = pd.read_csv("Binance_ETHUSDT_d.csv")

avg = 0
daily_pos = []
for index, row in data.iterrows():
    if row['close'] >= row['open']:
        pos_diff = row['close'] - row['open']
        if index == 0:
            prev_vol = data.loc()[index - 1]
        else:
            prev_vol = row['Volume']
        avg += pos_diff
        daily_pos.append(pos_diff)
avg = avg / len(data)

print("Avg Positive Daily Change (USD)")
print(avg)
print("Number of days closed above average")

days_above_avg = 0
for day in daily_pos:
    if day >= avg:
        days_above_avg += 1

print(days_above_avg, "out of", len(data))
