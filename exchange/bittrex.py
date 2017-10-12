from exchange.base import BaseApi, Pair
from exchange.exchanges import BaseExchangeException


class BittrexApiException(BaseExchangeException):
    pass


class BittrexApi(BaseApi):
    name = 'bittrex'
    url = 'https://bittrex.com/'

    async def tradable_pairs(self) -> set:
        response = await self.get('https://bittrex.com/api/v1.1/public/getmarkets')
        result = response['result']
        return set(
            Pair(
                self._substitute(i['BaseCurrency']),
                self._substitute(i['MarketCurrency']),
            ) for i in result
        )

    def _raise_if_error(self, response: dict):
        if not response['success']:
            raise BittrexApiException(response['message'])

    def _substitute(self, currency) -> str:
        return currency

    def ticker_url(self, pair: Pair) -> str:
        return f'https://bittrex.com/Market/Index?MarketName={pair.base}-{pair.quote}'
