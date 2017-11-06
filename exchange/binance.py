from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class BinanceApiException(BaseExchangeException):
    pass


class BinanceApi(BaseApi):
    @property
    def name(self):
        return 'binance'

    @property
    def md_link(self):
        return self.markdown_url('Binance', 'https://www.binance.com/')

    async def tradable_pairs(self) -> set:
        response = await self.get('https://www.binance.com/exchange/public/product')
        result = response['data']
        return set(
            Pair(
                i['baseAsset'],
                i['quoteAsset'],
            ) for i in result
        )

    def _raise_if_error(self, response: dict):
        if not response or 'data' not in response:
            raise BinanceApiException(response.get('msg', 'Empty response'))

    def ticker_url(self, pair: Pair) -> str:
        return f'https://www.binance.com/trade.html?symbol={pair.base}_{pair.quote}'
