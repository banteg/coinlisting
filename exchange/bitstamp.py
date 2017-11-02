from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class BitstampApiException(BaseExchangeException):
    pass


class BitstampApi(BaseApi):
    name = 'bitstamp'
    url = 'https://www.bitstamp.net/'

    async def tradable_pairs(self) -> set:
        result = await self.get('https://www.bitstamp.net/api/v2/trading-pairs-info/')
        return set(
            Pair(
                i['name'].split('/')[0],
                i['name'].split('/')[1],
            ) for i in result
        )

    def _raise_if_error(self, response: dict):
        if not isinstance(response, list):
            raise BitstampApiException('bitstamp api changed')

    def ticker_url(self, pair: Pair) -> str:
        return 'https://www.bitstamp.net/market/tradeview/'
