import asyncpg

import settings
from exchange.base import Pair

pool = None  # asyncpg connection pool


async def create_tables():
    async with pool.acquire() as conn:
        await conn.fetch(
            '''CREATE TABLE IF NOT EXISTS pair(
                exchange_name VARCHAR,
                base VARCHAR,
                quote VARCHAR,
                PRIMARY KEY (exchange_name, base, quote))'''
        )


async def init_db():
    global pool
    pool = await asyncpg.create_pool(settings.DATABASE_URL)
    await create_tables()


async def get_pairs(exchange_name):
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            '''SELECT base, quote
               FROM pair
               WHERE exchange_name = $1''',
            exchange_name
        )
        return {Pair(row['base'], row['quote']) for row in rows}


async def update_pairs(exchange_name, pairs):
    async with pool.acquire() as conn:
        await conn.executemany(
            '''INSERT INTO pair (exchange_name, base, quote)
               VALUES ($1, $2, $3) 
               ''',
            ((exchange_name, p.base, p.quote) for p in pairs)
        )
