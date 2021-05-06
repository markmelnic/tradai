import json, requests
from envars import API_KEY
from urllib.parse import urlencode

BASE_URL = "https://www.alphavantage.co/query?"

def cur(data: dict, special: str = None) -> float:
    _itv = INTERVAL
    if special:
        _itv = special

    for d in data[f"Time Series ({_itv})"]:
        return float(data[f"Time Series ({_itv})"][d]['5. adjusted close'])

def ma_calc(data: dict, period: float, special: str = None) -> float:
    _itv = INTERVAL
    if special:
        _itv = special

    for d in data[f"Time Series ({_itv})"]:
        total = 0
        for i in range(period):
            point = data[f"Time Series ({_itv})"][d]
            total += (float(point['2. high']) + float(point['3. low'])) / 2
        return total / period

INTERVAL = '1min'
params = urlencode({
    'function': 'TIME_SERIES_INTRADAY',
    'outputsize': 'full', # compact
    'adjusted': 'true',
    'interval': INTERVAL,
    'symbol': 'TSLA',
    'apikey': API_KEY})

params = urlencode({
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'outputsize': 'compact',
    'symbol': 'TSLA',
    'apikey': API_KEY})

print(BASE_URL + params)
res = requests.get(BASE_URL + params)
data = json.loads(res.content.decode("utf-8"))

with open('data.json', 'w') as _:
    _.write(json.dumps(data))

print("Current price is", cur(data, special="Daily"))
print("MA for period 8 is", ma_calc(data, 8, special="Daily"))
print("MA for period 20 is", ma_calc(data, 20, special="Daily"))
print("MA for period 50 is", ma_calc(data, 50, special="Daily"))
print("MA for period 200 is", ma_calc(data, 200, special="Daily"))
