from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class BitstampApiException(BaseExchangeException):
    pass


class BitstampPairNamesException(BitstampApiException):
    pass


class BitstampApi(BaseApi):
    @property
    def name(self):
        return 'bitstamp'

    @property
    def md_link(self):
        return self.markdown_url('Bitstamp', 'https://www.bitstamp.net/')

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

    async def coin_name(self, symbol: str) -> str:
        trading_pairs = await self.get('https://www.bitstamp.net/api/v2/trading-pairs-info/')
        if not isinstance(trading_pairs, list):
            raise BitstampPairNamesException('bitstamp api changed')
        description = next((i['description'] for i in trading_pairs if i['name'].startswith(symbol)), None)
        if not description:
            raise BitstampPairNamesException(f'cannot find coin {symbol!r}')
        return description.split('/')[0].strip()  # "Litecoin / U.S. dollar"
