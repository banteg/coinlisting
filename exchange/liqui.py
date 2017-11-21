from aiocfscrape import CloudflareScraper

from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class LiquiApiException(BaseExchangeException):
    pass


class LiquiPairNamesException(LiquiApiException):
    pass


class LiquiApi(BaseApi):
    @property
    def name(self):
        return 'liqui'

    @property
    def md_link(self):
        return self.markdown_url('Liqui', 'https://liqui.io/')

    async def tradable_pairs(self) -> set:
        response = await self.get('https://api.liqui.io/api/3/info')
        result = response['pairs']
        return set(
            Pair(
                pair.split('_')[0],
                pair.split('_')[1],
            ) for pair in result
        )

    def _raise_if_error(self, response: dict):
        if 'error' in response:
            raise LiquiApiException(response['error'])

    def ticker_url(self, pair: Pair) -> str:
        return f'https://liqui.io/#/exchange/{pair.base}_{pair.quote}'

    async def coin_name(self, symbol: str) -> str:
        try:
            async with CloudflareScraper() as session:
                async with session.get('https://liqui.io/Market/Currencies/') as resp:
                    currencies = await resp.json()
        except Exception as e:
            raise LiquiPairNamesException(e)
        coin_name = next((i['Name'] for i in currencies if i['Symbol'] == symbol), None)
        if not coin_name:
            raise LiquiPairNamesException(f'cannot find coin {symbol!r}')
        return coin_name
