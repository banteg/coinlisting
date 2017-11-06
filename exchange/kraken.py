from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class KrakenApiException(BaseExchangeException):
    pass


class KrakenApi(BaseApi):
    @property
    def name(self):
        return 'kraken'

    @property
    def md_link(self):
        return self.markdown_url('Kraken', 'https://www.kraken.com/')

    async def tradable_pairs(self) -> set:
        response = await self.get('https://api.kraken.com/0/public/AssetPairs')
        result = response['result']
        return set(
            Pair(
                pair_info['base'],
                pair_info['quote'],
            ) for pair, pair_info in result.items()
        )

    def _raise_if_error(self, response: dict):
        if response['error']:
            raise KrakenApiException('\n'.join(response['error']))

    def ticker_url(self, pair: Pair) -> str:
        return 'https://www.kraken.com/charts'
