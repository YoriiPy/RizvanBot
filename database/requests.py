import aiosqlite
import asyncio

from _testcapi import awaitType

DB_NAME = 'database.db'

async def add_user(user_id: int, username: str) -> None:
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''INSERT OR IGNORE INTO users (user_id, username) VALUES (?,?)''', (user_id, username))
        await db.commit()
# РАССЫЛКА
async def get_user_broadcast(user_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT broadcast FROM users WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return result[0]
            return False

async def get_users_broadcast() -> bool | list[tuple[int]]:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('''SELECT user_id FROM users WHERE broadcast = 1''') as cursor:
            result = await cursor.fetchone()
            if result:
                list_user_id = [result[0] for result in result]
                return list_user_id
            return False

async def update_state_stream(number):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE streams SET is_live = ?", (number))



