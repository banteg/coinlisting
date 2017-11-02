from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class GateApiException(BaseExchangeException):
    pass


class GateApi(BaseApi):
    name = 'gate'
    url = 'https://gate.io/'

    async def tradable_pairs(self) -> set:
        result = await self.get('http://data.gate.io/api2/1/pairs')
        return set(
            Pair(
                pair.split('_')[0],
                pair.split('_')[1],
            ) for pair in result
        )

    def _raise_if_error(self, response: dict):
        if not isinstance(response, list):
            raise GateApiException('gate api changed')

    def ticker_url(self, pair: Pair) -> str:
        return f'https://gate.io/trade/{pair.base}_{pair.quote}'
