import asyncio
from abc import ABC, abstractmethod
from collections import namedtuple
from logging import getLogger

import aiohttp
from aiohttp import ClientSession

from exchange.exceptions import WrongContentTypeException, InvalidResponseException, BaseExchangeException
from settings import REQUEST_ATTEMPTS_LIMIT


class Pair(namedtuple('Pair', ['base', 'quote'])):
    def __new__(cls, base, quote):
        return super(Pair, cls).__new__(cls, base.upper(), quote.upper())


class BaseApi(ABC):
    @property
    @abstractmethod
    def name(self):
        '''Return exchange's name.'''

    @abstractmethod
    async def tradable_pairs(self) -> set:
        '''Returns a list of exchange tradable pairs as set.'''

    @abstractmethod
    def _raise_if_error(self, response: dict):
        '''Raises BaseExchangeException if there is an errors in API response.
        :raises BaseExchangeException:
        '''

    @abstractmethod
    def ticker_url(self, pair: Pair) -> str:
        '''Returns exchange ticker url for specified pair.'''

    @abstractmethod
    async def coin_name(self, symbol: str) -> str:
        '''Returns base coin name for coin symbol (i.e. 'Litecoin' for 'LTC' if possible else empty string.'''

    @property
    @abstractmethod
    def md_link(self):
        '''Return markdown link to exchange.'''

    @staticmethod
    def markdown_url(title, url):
        return f'[{title}]({url})'

    async def request(self, url, headers, check_response, method='get', data=None):
        attempt, delay = 1, 1
        async with ClientSession() as s:
            session_method = s.__getattribute__(method.lower())
            while True:
                try:
                    resp = await session_method(url=url, headers=headers, data=data)
                    if resp.content_type != 'application/json':
                        raise WrongContentTypeException(f'Unexpected content type {resp.content_type!r} at URL {url}.')
                    json_resp = await resp.json()
                    if check_response:
                        self._raise_if_error(json_resp)
                    return json_resp
                except (aiohttp.client_exceptions.ClientResponseError,
                        aiohttp.client_exceptions.ClientConnectorError,
                        BaseExchangeException) as e:
                    getLogger().error(f'attempt {attempt}/{REQUEST_ATTEMPTS_LIMIT}, next in {delay} seconds...')
                    getLogger().exception(e)
                    attempt += 1
                    if attempt > REQUEST_ATTEMPTS_LIMIT:
                        raise InvalidResponseException(e)
                    await asyncio.sleep(delay)
                    delay *= 2

    async def post(self, url: str, check_response=True, headers: dict = None, data: dict = None) -> dict:
        return await self.request(url, headers, check_response, 'post', data)

    async def get(self, url: str, check_response=True, headers: dict = None) -> dict:
        return await self.request(url, headers, check_response)
