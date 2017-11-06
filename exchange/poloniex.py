from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class PoloniexApiException(BaseExchangeException):
    pass


class PoloniexApi(BaseApi):
    @property
    def name(self):
        return 'poloniex'

    @property
    def md_link(self):
        return self.markdown_url('Poloniex', 'https://poloniex.com/')

    async def tradable_pairs(self) -> set:
        result = await self.get('https://poloniex.com/public?command=returnTicker')
        return set(
            Pair(
                pair.split('_')[0],
                pair.split('_')[1],
            ) for pair in result
        )

    def _raise_if_error(self, response: dict):
        if not response or 'error' in response:
            raise PoloniexApiException(response.get('error', 'Empty response'))

    def ticker_url(self, pair: Pair) -> str:
        return f'https://poloniex.com/exchange#{pair.base}_{pair.quote}'
