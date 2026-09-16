from unittest import result

import aiosqlite
import asyncio

from _testcapi import awaitType
from aiosqlite import cursor

DB_NAME = 'database.db'


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
# СТРИМ
async def update_state_stream(number):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE streams SET is_live = ?", (number))

async def get_url_stream():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM streams") as cursor:
            result = (await cursor.fetchone())[0]
            if result:
                return result

async def edit_url_stream(url: str):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM streams") as cursor:
            result = await cursor.fetchone()
            if result:
                await db.execute("UPDATE streams SET url = ?", (url, ))
                await db.commit()
            else:
                await db.execute("INSERT INTO streams (url) VALUES (?)", (url, ))

# ДОБАВЛЕНИЕ
async def add_admin(user_id: int, username: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET class = ? WHERE user_id = ?", ('admin',user_id))

async def add_main_admin(user_id: int, username: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET class = ? WHERE user_id = ?", ('main_admin',user_id))

async def add_user(user_id: int, username: str) -> None:
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''INSERT OR IGNORE INTO users (user_id, username) VALUES (?,?)''', (user_id, username))
        await db.commit()
# ПОИСК
async def search_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT 1 FROM users WHERE user_id = ?", ('user',)) as cursor:
            result = await cursor.fetchone()
            if result == 1:
                return True
async def search_admin(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT 1 FROM users WHERE class = ?", ('admin',)) as cursor:
            result = await cursor.fetchone()
            if result == 1:
                return True

async def search_main_admin(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute("SELECT 1 FROM users WHERE class = ?", ('main_admin',))



