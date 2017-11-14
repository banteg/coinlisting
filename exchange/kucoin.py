from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class KucoinApiException(BaseExchangeException):
    pass


class KucoinPairNamesException(KucoinApiException):
    pass


class KucoinApi(BaseApi):
    @property
    def name(self):
        return 'kucoin'

    @property
    def md_link(self):
        return self.markdown_url('Kucoin', 'https://www.kucoin.com/')

    async def tradable_pairs(self) -> set:
        response = await self.get('https://api.kucoin.com/v1/market/open/symbols')
        result = response['data']
        return set(
            Pair(
                i['coinType'],
                i['coinTypePair'],
            ) for i in result
        )

    def _raise_if_error(self, response: dict):
        if not response or 'data' not in response or not response['success']:
            raise KucoinApiException(response.get('msg', 'Empty response'))

    def ticker_url(self, pair: Pair) -> str:
        return f'https://www.kucoin.com/#/trade/{pair.base}-{pair.quote}'

    async def coin_name(self, symbol: str) -> str:
        response = await self.get('https://api.kucoin.com/v1/market/open/coins-list')
        if not response['success']:
            raise KucoinPairNamesException(response['msg'])
        trading_pairs = response['data']
        coin_name = next((i['name'] for i in trading_pairs if i['coin'] == symbol), None)
        if not coin_name:
            raise KucoinPairNamesException(f'cannot find coin {symbol!r}')
        return coin_name
