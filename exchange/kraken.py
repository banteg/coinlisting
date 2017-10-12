from exchange.base import BaseApi, Pair
from exchange.exchanges import BaseExchangeException


class KrakenApiException(BaseExchangeException):
    pass


class KrakenApi(BaseApi):
    name = 'kraken'
    url = 'https://www.kraken.com/'

    substitute_rules = {
        'KFEE': 'FEE',
        'XDAO': 'DAO',
        'XETC': 'ETC',
        'XETH': 'ETH',
        'XICN': 'ICN',
        'XLTC': 'LTC',
        'XMLN': 'MLN',
        'XNMC': 'NMC',
        'XREP': 'REP',
        'XXBT': 'BTC',  # !
        'XXDG': 'XDG',
        'XXLM': 'XLM',
        'XXMR': 'XMR',
        'XXRP': 'XRP',
        'XXVN': 'XVN',
        'XZEC': 'ZEC',
        'ZCAD': 'CAD',
        'ZEUR': 'EUR',
        'ZGBP': 'GBP',
        'ZJPY': 'JPY',
        'ZKRW': 'KRW',
        'ZUSD': 'USD'
    }

    async def tradable_pairs(self) -> set:
        response = await self.get('https://api.kraken.com/0/public/AssetPairs')
        result = response['result']
        return set(
            Pair(
                self._substitute(pair_info['base']),
                self._substitute(pair_info['quote']),
            ) for pair, pair_info in result.items()
        )

    def _raise_if_error(self, response: dict):
        if response['error']:
            raise KrakenApiException('\n'.join(response['error']))

    def _substitute(self, currency) -> str:
        return self.substitute_rules.get(currency, currency)

    def ticker_url(self, pair: Pair) -> str:
        return 'https://www.kraken.com/charts'
