from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class LiquiApiException(BaseExchangeException):
    pass


class LiquiApi(BaseApi):
    name = 'liqui'
    url = 'https://liqui.io/'

    async def tradable_pairs(self) -> set:
        response = await self.get('https://api.liqui.io/api/3/info')
        result = response['pairs']
        return set(
            Pair(
                self._substitute(pair.split('_')[0]),
                self._substitute(pair.split('_')[1]),
            ) for pair in result
        )

    def _raise_if_error(self, response: dict):
        if 'error' in response:
            raise LiquiApiException(response['error'])

    def _substitute(self, currency) -> str:
        return currency.upper()

    def ticker_url(self, pair: Pair) -> str:
        return f'https://liqui.io/#/exchange/{pair.base}_{pair.quote}'
