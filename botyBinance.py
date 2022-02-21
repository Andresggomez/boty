import config

class RobotBinance:
    """
    Bot para crear ordenes de compra y venta en RobotBinance

    """
    __api_key = config.API_KEY
    __api_secret = config.API_SECRET_KEY

    def __init__(self, pair: str, temporality: str):
        self.pair= pair.upper()
        self.temporality= temporality
        self.symbol= self.pair.removesuffix("USDT")

    


bot = RobotBinance("btcusdt", "4h")
print(bot.pair)
