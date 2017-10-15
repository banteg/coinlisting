from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class EtherdeltaApiException(BaseExchangeException):
    pass


class EtherdeltaApi(BaseApi):
    name = 'etherdelta'
    url = 'https://etherdelta.com/'

    async def tradable_pairs(self) -> set:
        result = await self.get('https://api.etherdelta.com/returnTicker')
        return set(
            Pair(
                self._substitute(pair.split('_')[0]),
                self._substitute(pair.split('_')[1]),
            ) for pair in result
        )

    def _raise_if_error(self, response: dict):
        if not len(response):
            raise EtherdeltaApiException('Empty response')

    def _substitute(self, currency) -> str:
        return currency

    def ticker_url(self, pair: Pair) -> str:
        return f'https://etherdelta.com/#{pair.base}-{pair.quote}'
