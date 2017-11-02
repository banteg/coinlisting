from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class BitfinexApiException(BaseExchangeException):
    pass


class BitfinexApi(BaseApi):
    name = 'bitfinex'
    url = 'https://www.bitfinex.com/'

    async def tradable_pairs(self) -> set:
        result = await self.get('https://api.bitfinex.com/v1/symbols')
        return set(
            Pair(
                i[:3].upper(),
                i[3:].upper()
            ) for i in result
        )

    def _raise_if_error(self, response: dict):
        if not isinstance(response, list):
            raise BitfinexApiException('bitfinex api changed')

    def ticker_url(self, pair: Pair) -> str:
        return f'https://www.bitfinex.com/trading/{pair.base}{pair.quote}'
