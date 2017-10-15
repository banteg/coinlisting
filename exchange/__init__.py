from exchange.binance import BinanceApi
from exchange.bittrex import BittrexApi
from exchange.kraken import KrakenApi
from exchange.liqui import LiquiApi
from exchange.poloniex import PoloniexApi

exchanges = [KrakenApi, LiquiApi, BittrexApi, PoloniexApi, BinanceApi]
