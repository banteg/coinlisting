from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class BitfinexApiException(BaseExchangeException):
    pass


class BitfinexPairNamesException(BitfinexApiException):
    pass


class BitfinexApi(BaseApi):
    @property
    def name(self):
        return 'bitfinex'

    @property
    def md_link(self):
        return self.markdown_url('Bitfinex', 'https://www.bitfinex.com/')

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

    async def coin_name(self, symbol: str) -> str:
        response = await self.get('https://www.bitfinex.com/account/_bootstrap/', check_response=False)
        if not response or 'nice_ccy_names' not in response:
            raise BitfinexPairNamesException('bitfinex api changed')
        currencies = response['nice_ccy_names']
        if symbol not in currencies:
            raise BitfinexPairNamesException(f'cannot find coin {symbol!r}')
        return currencies.get(symbol, '')
