from exchange.binance import BinanceApi
from exchange.bitfinex import BitfinexApi
from exchange.bitstamp import BitstampApi
from exchange.bittrex import BittrexApi
from exchange.cryptopia import CryptopiaApi
from exchange.gate import GateApi
from exchange.kraken import KrakenApi
from exchange.kucoin import KucoinApi
from exchange.liqui import LiquiApi
from exchange.poloniex import PoloniexApi
from exchange.radarrelay import RadarRelayApi
from exchange.ethfinex import EthfinexApi

exchanges = [
    KrakenApi,
    LiquiApi,
    BittrexApi,
    PoloniexApi,
    BinanceApi,
    BitfinexApi,
    BitstampApi,
    CryptopiaApi,
    GateApi,
    RadarRelayApi,
    KucoinApi,
    EthfinexApi,
]
