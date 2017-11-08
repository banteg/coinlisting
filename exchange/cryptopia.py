from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class CryptopiaApiException(BaseExchangeException):
    pass


class CryptopiaPairNamesException(CryptopiaApiException):
    pass


class CryptopiaApi(BaseApi):
    @property
    def name(self):
        return 'cryptopia'

    @property
    def md_link(self):
        return self.markdown_url('Cryptopia', 'https://www.cryptopia.co.nz/')

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

    async def coin_name(self, symbol: str) -> str:
        response = await self.get('https://www.cryptopia.co.nz/api/GetTradePairs')
        if not response['Success']:
            raise CryptopiaPairNamesException(response['Message'])
        trading_pairs = response['Data']
        coin_name = next((i['Currency'] for i in trading_pairs if i['Label'].startswith(symbol)), None)
        if not coin_name:
            raise CryptopiaPairNamesException(f'cannot find coin {symbol!r}')
        return coin_name
