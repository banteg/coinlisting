from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class BittrexApiException(BaseExchangeException):
    pass


class BittrexApi(BaseApi):
    @property
    def name(self):
        return 'bittrex'

    @property
    def md_link(self):
        return self.markdown_url('Bittrex', 'https://bittrex.com/')

    async def tradable_pairs(self) -> set:
        response = await self.get('https://bittrex.com/api/v1.1/public/getmarkets')
        result = response['result']
        return set(
            Pair(
                i['BaseCurrency'],
                i['MarketCurrency'],
            ) for i in result
        )

    def _raise_if_error(self, response: dict):
        if not response['success']:
            raise BittrexApiException(response['message'])

    def ticker_url(self, pair: Pair) -> str:
        return f'https://bittrex.com/Market/Index?MarketName={pair.base}-{pair.quote}'
