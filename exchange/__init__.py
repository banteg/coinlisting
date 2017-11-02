from exchange.binance import BinanceApi
from exchange.bitfinex import BitfinexApi
from exchange.bitstamp import BitstampApi
from exchange.bittrex import BittrexApi
from exchange.cryptopia import CryptopiaApi
from exchange.kraken import KrakenApi
from exchange.liqui import LiquiApi
from exchange.poloniex import PoloniexApi

exchanges = [
    KrakenApi,
    LiquiApi,
    BittrexApi,
    PoloniexApi,
    BinanceApi,
    BitfinexApi,
    BitstampApi,
    CryptopiaApi
]
