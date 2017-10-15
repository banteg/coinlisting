from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class BinanceApiException(BaseExchangeException):
    pass


class BinanceApi(BaseApi):
    name = 'binance'
    url = 'https://www.binance.com/'

    async def tradable_pairs(self) -> set:
        response = await self.get('https://www.binance.com/exchange/public/product')
        result = response['data']
        return set(
            Pair(
                self._substitute(i['baseAsset']),
                self._substitute(i['quoteAsset']),
            ) for i in result
        )

    def _raise_if_error(self, response: dict):
        if not response or 'data' not in response:
            BinanceApiException(response.get('msg', 'Empty response'))

    def _substitute(self, currency) -> str:
        return currency

    def ticker_url(self, pair: Pair) -> str:
        return f'https://www.binance.com/trade.html?symbol={pair.base}_{pair.quote}'
