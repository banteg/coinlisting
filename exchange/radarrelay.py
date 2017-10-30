from exchange.base import BaseApi, Pair
from exchange.exceptions import BaseExchangeException


class RadarRelayApiException(BaseExchangeException):
    pass


class RadarRelayApi(BaseApi):
    name = 'radar_relay'
    url = 'https://app.radarrelay.com'

    async def tradable_pairs(self) -> set:
        response = await self.get(
            'https://api.radarrelay.com/v1/info/tokens',
            headers={'Origin': 'https://app.radarrelay.com'}
        )
        return set(
            Pair(
                pair['symbol'],
                'WETH',
            ) for pair in response
        )

    def _raise_if_error(self, response: dict):
        if not isinstance(response, list):
            RadarRelayApiException('radar relay api changed')

    def _substitute(self, currency) -> str:
        return currency

    def ticker_url(self, pair: Pair) -> str:
        return f'https://app.radarrelay.com/#{pair.base}-{pair.quote}'
