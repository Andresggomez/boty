#strategy.py
import pandas as pd
from talib import EMA, RSI, MACD
import pandas_ta as ta
import matplotlib.pyplot as plt


class Indicadores:

    def __init__(self, data):

        self.close = data.get('Close')
        self.open = data.get('Open')
        self.high = data.get('Higt')
        self.low = data.get('Low')
        self.data = data
        self.volume = data.get('Volume')
        self.open_time = data.get('Open Time')
        self.trade = data.get('Number of trades')


    def ema(self, timeperiod: int):
        return EMA(
            self.close,
            timeperiod=timeperiod
        ).iloc[-1]

    def emaplot(self, timeperiod: int):
        return EMA(
            self.close,
            timeperiod=timeperiod
        )

    def rsi(self, timeperiod: int):
        return RSI(
            self.close,
            timeperiod=timeperiod
        ).iloc[-1]

    def rsiplot(self, timeperiod: int):
        return RSI(
            self.close,
            timeperiod=timeperiod
        )

    def adx(self):
        return ta.adx(self.high, self.low, self.close)['ADX_14']

    def crearDatos(self):

        ema200 = self.emaplot(200)
        ema50 = self.emaplot(50)
        ema20 = self.emaplot(20)
        rsi = self.rsiplot(14)
        volumen = self.volume
        precio = self.close
        trades = self.trade

        df = pd.concat([trades, precio, volumen, ema200, ema50, ema20, rsi], axis=1)

        df.to_csv('data.csv')

        return df