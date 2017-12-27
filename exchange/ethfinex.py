from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class EthfinexApiException(BaseExchangeException):
    pass


class EthfinexPairNamesException(EthfinexApiException):
    pass


class EthfinexApi(BaseApi):
    @property
    def name(self):
        return 'ethfinex'

    @property
    def md_link(self):
        return self.markdown_url('Ethfinex', 'https://www.ethfinex.com')

    async def tradable_pairs(self) -> set:
        result = await self.get('https://api.ethfinex.com/v1/symbols')
        return set(
            Pair(
                i[:3].upper(),
                i[3:].upper()
            ) for i in result
        )

    def _raise_if_error(self, response: dict):
        if not isinstance(response, list):
            raise EthfinexApiException('ethfinex api changed')

    def ticker_url(self, pair: Pair) -> str:
        return f'https://www.ethfinex.com/trading/{pair.base}{pair.quote}'

    async def coin_name(self, symbol: str) -> str:
        response = await self.get('https://www.ethfinex.com/account/_bootstrap/', check_response=False)
        if not response or 'nice_ccy_names' not in response:
            raise EthfinexPairNamesException('ethfinex api changed')
        currencies = response['nice_ccy_names']
        if symbol not in currencies:
            raise EthfinexPairNamesException(f'cannot find coin {symbol!r}')
        return currencies.get(symbol, '')
