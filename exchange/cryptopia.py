from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class CryptopiaApiException(BaseExchangeException):
    pass


class CryptopiaApi(BaseApi):
    name = 'cryptopia'
    url = 'https://www.cryptopia.co.nz/'

    async def tradable_pairs(self) -> set:
        response = await self.get('https://www.cryptopia.co.nz/api/GetTradePairs')
        result = response['Data']
        return set(
            Pair(
                i['Symbol'],
                i['BaseSymbol'],
            ) for i in result
        )

    def _raise_if_error(self, response: dict):
        if not response or 'Data' not in response or not response['Success']:
            raise CryptopiaApiException(response.get('Message', 'Empty response'))

    def ticker_url(self, pair: Pair) -> str:
        return f'https://www.cryptopia.co.nz/Exchange/?market={pair.base}_{pair.quote}'
