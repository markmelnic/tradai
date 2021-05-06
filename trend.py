import json
from rich import print
from enum import Enum
from tda import auth, client
from datetime import datetime

from envars import API_KEY1

token_path = 'token.pickle'
redirect_uri = 'http://127.0.0.1:5000/call'

class Trends(Enum):
    D = 0 # downtrend
    U = 1 # uptrend
    L = 2 # liniar

try:
    c = auth.client_from_token_file(token_path, API_KEY1)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome() as driver:
        c = auth.client_from_login_flow(
            driver, API_KEY1, redirect_uri, token_path,
            redirect_wait_time_seconds=0.1, max_waits=3000, asyncio=False, token_write_func=None)

r = c.get_price_history('SPY',
        period=client.Client.PriceHistory.Period.ONE_DAY,
        frequency=client.Client.PriceHistory.Frequency.EVERY_MINUTE)
assert r.status_code == 200, r.raise_for_status()

with open("data.json", "w") as jfile:
    jfile.write(json.dumps(r.json(), indent=4))

prevclose = 0
ut, dt, lt = [], [], []
trend, prevtrend, tendency = Trends.L, Trends.L, Trends.L
for i, c in enumerate(r.json()['candles']):
    close = c['close']
    time = datetime.fromtimestamp(c['datetime'] / 1e3).strftime('%H:%M')

    # determine trend
    temptrend = trend
    if trend == Trends.L:
        if close == prevclose:
            lt.append(i) # start uptrend
        elif close > prevclose:
            if tendency == Trends.U:
                print(f"{i} {time} [blue]LINEAR ENDED[/blue] at {prevclose}")
                trend, prevtrend = Trends.U, Trends.U
                ut, dt = [], []
            else:
                tendency = Trends.U
            lt.append(i) # start uptrend
        elif close < prevclose:
            if tendency == Trends.D:
                print(f"{i} {time} [blue]LINEAR ENDED[/blue] at {prevclose}")
                trend, prevtrend = Trends.D, Trends.D
                ut, dt = [], []
            else:
                tendency = Trends.D
            lt.append(i) # start downtrend
    else:
        if close == prevclose:
            dt, trend = [], Trends.L
        elif close > prevclose:
            if((trend == Trends.U and prevtrend == Trends.D)
            or (trend == Trends.U and prevtrend == Trends.L)):
                print(f"{i} {time} [green]DOWNTREND ENDED[/green] at {prevclose}")
                ut, lt, trend = [], [], Trends.L
            elif trend == Trends.U:
                ut.append(i) # continue uptrend
        elif close < prevclose:
            if((trend == Trends.D and prevtrend == Trends.U)
            or (trend == Trends.D and prevtrend == Trends.L)):
                print(f"{i} {time} [red]UPTREND ENDED[/red] at {prevclose}")
                dt, lt, trend = [], [], Trends.L
            elif trend == Trends.D:
                dt.append(i) # continue downtrend
    prevclose = close
    prevtrend = temptrend
