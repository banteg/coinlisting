import asyncio
from abc import ABC, abstractmethod
from collections import namedtuple
from logging import getLogger

import aiohttp
from aiohttp import ClientSession

from exchange.exceptions import WrongContentTypeException, InvalidResponseException, BaseExchangeException
from settings import REQUEST_ATTEMPTS_LIMIT

Pair = namedtuple('Pair', ['base', 'quote'])


class BaseApi(ABC):
    name = None
    url = None

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

    async def request(self, url, headers, method='get', data=None):
        attempt, delay = 1, 1
        async with ClientSession() as s:
            session_method = s.__getattribute__(method.lower())
            while True:
                try:
                    resp = await session_method(url=url, headers=headers, data=data)
                    if resp.content_type != 'application/json':
                        raise WrongContentTypeException(f'Unexpected content type {resp.content_type!r} at URL {url}.')
                    json_resp = await resp.json()
                    self._raise_if_error(json_resp)
                    return json_resp
                except (aiohttp.client_exceptions.ClientResponseError, BaseExchangeException) as e:
                    getLogger().error(f'attempt {attempt}/{REQUEST_ATTEMPTS_LIMIT}, next in {delay} seconds...')
                    getLogger().exception(e)
                    attempt += 1
                    if attempt > REQUEST_ATTEMPTS_LIMIT:
                        raise InvalidResponseException(e)
                    await asyncio.sleep(delay)
                    delay *= 2

    async def post(self, url: str, headers: dict = None, data: dict = None) -> dict:
        return await self.request(url, headers, 'post', data)

    async def get(self, url: str, headers: dict = None) -> dict:
        return await self.request(url, headers)
