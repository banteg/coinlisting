import asyncio
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
        for api_cls in exchanges:
            api = api_cls()
            try:
                api_pairs = await api.tradable_pairs()
            except BaseExchangeException as e:
                getLogger().exception(e)
                continue
            db_pairs = await db.get_pairs(api.name)
            if not db_pairs:
                # initial launch, don't send message to channel, only put pairs to db
                await db.update_pairs(api.name, api_pairs)
                getLogger().info(f'Initial launch, {len(api_pairs)} pairs added on exchange {api.name!r}.')
                continue

            new_pairs = api_pairs - db_pairs

            if new_pairs:
                getLogger().info(f'There is {len(new_pairs)} new pairs on exchange {api.name!r}')
                await db.update_pairs(api.name, new_pairs)
                getLogger().info('Pairs added to db.')
                for pair in new_pairs:
                    await self.send_message(self.compose_message(api, pair))
                    getLogger().info(f'Notification about pair {pair} has been sent to channel.')
                continue
            getLogger().info(f'There is no new pairs on exchange {api.name!r}.')

    async def periodic(self, interval=None):
        while True:
            getLogger().info('sleeping')
            await asyncio.sleep(interval or settings.CHECK_INTERVAL)
            await self.check()

    async def send_message(self, coin_info):
        await self.channel.send_text(coin_info, parse_mode='Markdown')

    @staticmethod
    def compose_message(api: BaseApi, pair: Pair) -> str:
        pair_name = f'{pair.base}/{pair.quote}'
        return f'[{pair_name}]({api.ticker_url(pair)}) listed on [{api.name.title()}]({api.url})'


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
