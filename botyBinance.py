from strategy import Indicadores
from binance.spot import Spot
import pandas as pd  # Pandas
from time import sleep
import config
import requests

class BotyBinance:
    """
    Bot de señales, compras / ventas en el mercado de Criptomonedas VOLUMEN TOTAL $xx millones
    """
    # Variables de clase privadas __apis
    __api_key = config.API_KEY  # API de usuario Publica
    __api_secret = config.API_SECRET_KEY
    binance_client = Spot(key=__api_key, secret=__api_secret)  # guarda la conexion

    def __init__(self, pair: str, temporality: str):  # Inicializa parametros

        # Variables de instancia
        self.pair = pair.upper()  # BTC/USDT
        self.temporality = temporality  # 4h, 15m
        self.symbol = self.pair.removesuffix("USDT")

    def _request(self, endpoint: str, parameters: dict = None):  # Conexion usuario/API
        """
        #endpoits son las funiones de la api, account, klines etc.
        Log de errores
        :return: response con informacion de errores en casos fallido, 
        """
        try:
            response = getattr(self.binance_client, endpoint)
            return response() if parameters is None else response(**parameters)
        except:
            print(f'el endopoint {endpoint} ha fallado.\n Parametros: {parameters}\n\n')
            sleep(2)

    def binance_account(self):
        """
        Devuelve estado de cuenta general con referencia a la API
        :return: Cuenta de binance. ->Dic [datos]
        """

        return self._request('account')

    def criptomonedas(self) -> list[dict]:
        """
        Devuelve una lista de diccionarios en con las cuentas que tienen un saldo
        :return: Critomonedas con saldo 
        """
        lista = self.binance_account().get('balances')

        return [crypto for crypto in lista if float(crypto.get('free')) > 0]

    def precio(self, pair: str = None):
        """
        Calcula precio en tiempo real de un activo digital pair:"BTCUSDT", temporality:"4h"
        :return: valor flotante del precio actual
        """

        symbol = self.pair if pair is None else pair

        return float(self._request('ticker_price', {'symbol': symbol.upper()}).get('price'))
    
    def candlestick(self, limit: int = 565) -> pd.DataFrame:
        """
        Se calcula el intervalo de tiempo de casa vela para analisar
        :return: Un data Frame de tipo pandas, un candle!

        """
        
        params = {
            'symbol': self.pair, 
            'interval': self.temporality,
            'limit': limit
        }
        
        candle = pd.DataFrame(self._request(
            'klines',
            params
        ),

            columns=[
                'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                'Taker buy quote asset volume', 'Ignore'
            ],
            dtype=float
        )
        return candle[['Open', 'High', 'Low', 'Close', 'Volume', 'Number of trades']]

#  pprint(bot.binance_account())
#  pprint(type(bot.binance_account()))
# pprint(bot.criptomonedas())  # saldos en crypto de la cuenta

#  pprint(bot.candlestick())
#  mensaje =  bot.candlestick()
#  bot.mensajeALerta(mensaje)
#  precioActual= bot.candlestick()
#  pprint(precioActual)
#  pprint(bot.precio())

#  Calcula el valor del indicador
#  pprint(Indicadores(bot.candlestick()).rsi(14))
 #Indicadores(bot.candlestick()).grafica_adx()

if __name__ == '__main__':

    bot = BotyBinance("btcusdt", "1m")  # Nombre y temporalidad

    print("Boty Online.... ----> btcusdt 1m \ncontador")
    compra = 0
    venta = 0
    poscicionLarga = 0
    poscicionCorta = 0
    columns = ['RSI', 'ESTADO', 'TENDENCIA', 'PRECIO', 'RECOMENDACION', 'CortoE', 'LargoE']

    #  LogBoty.csv
    df = pd.DataFrame(columns=columns)

    #  Calcular el valor de la ema20 fin de COBRAR C/V
    #  Calcular divergencias
    #  Mensajes
    #  email?


    def mensaje(msj):

        bot_token = config.bot_token
        bot_chatID = config.bot_chatID
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + msj

        response = requests.get(send_text)

        return response

    def info():

        return Indicadores(bot.candlestick()).crearDatos()

    #btc1m = info()
    
    ##
        ema200 = Indicadores(bot.candlestick()).ema(200)
        rsi = Indicadores(bot.candlestick()).rsi(14)
        precio = bot.precio()
        ultimo = len(df.index)
    
