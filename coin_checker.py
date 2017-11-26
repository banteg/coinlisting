import asyncio
from itertools import groupby
from logging import getLogger

from aiotg import Bot, logging

import db
import settings
from exchange import exchanges
from exchange.base import Pair, BaseApi
from exchange.exceptions import BaseExchangeException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(settings.BOT_NAME)


class CoinChecker:
    bot = Bot(settings.BOT_TOKEN)
    channel = bot.channel(settings.CHANNEL_ID)

    async def check(self):
        await asyncio.gather(
            *(self.fetch_api(api_cls) for api_cls in exchanges)
        )

    async def fetch_api(self, api_cls):
        api = api_cls()
        try:
            api_pairs = await api.tradable_pairs()
        except Exception as e:
            getLogger().exception(e)
            return
        db_pairs = await db.get_pairs(api.name)
        if not db_pairs:
            # initial launch, don't send message to channel, only put pairs to db
            await db.update_pairs(api.name, api_pairs)
            getLogger().info(f'[{api.name}] initial launch, {len(api_pairs)} pairs added')
            return

        new_pairs = api_pairs - db_pairs

        if not new_pairs:
            getLogger().info(f'[{api.name}] no new pairs')
            return

        getLogger().info(f'[{api.name}] {len(new_pairs)} new pairs')
        await db.update_pairs(api.name, new_pairs)
        getLogger().info(f'[{api.name}] {len(new_pairs)} pairs added to database')

        for base, pairs in self.group_pairs(new_pairs):
            try:
                coin_name = await api.coin_name(base)
            except BaseExchangeException as e:
                getLogger().exception(e)
                coin_name = ''
            msg = self.compose_message(api, pairs, coin_name)
            await self.send_message(msg)
            getLogger().info(f'[{api.name}] message {msg!r} send to the channel')

    async def periodic(self, interval=None):
        while True:
            getLogger().info('sleeping')
            await asyncio.sleep(interval or settings.CHECK_INTERVAL)
            await self.check()

    async def send_message(self, coin_info):
        await self.channel.send_text(coin_info, parse_mode='Markdown', disable_web_page_preview=True)

    @staticmethod
    def compose_message(api: BaseApi, pairs: [Pair], coin_name: str) -> str:
        ticker_url = ', '.join(
            api.markdown_url(f'{pair.base}/{pair.quote}', api.ticker_url(pair))
            for pair in pairs
        )
        if coin_name:
            return f'*{coin_name}* listed on {api.md_link}\n{ticker_url}'
        return f'{ticker_url} listed on {api.md_link}'

    @staticmethod
    def group_pairs(pairs):
        for base, pairs in groupby(sorted(pairs), lambda x: x.base):
            yield base, list(pairs)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.init_db())
    try:
        logger.info('bot started')
        checker = CoinChecker()
        loop.run_until_complete(checker.check())
        asyncio.ensure_future(checker.periodic(), loop=loop)
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        logger.info('bot stopped')
