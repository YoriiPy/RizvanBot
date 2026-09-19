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
        async with db.execute("SELECT user_id FROM users WHERE broadcast = 1'") as cursor:
            users = await cursor.fetchall()
            if users:
                list_user_id = [int(row[0]) for row in users]
                return list_user_id
            return []
# СТРИМ
async def update_state_stream(number):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE streams SET is_live = ?", (number))

async def get_channel_name():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM streams") as cursor:
            result = await cursor.fetchone()
            if result is None:
                await db.execute("INSERT INTO streams (url) VALUES (?)", ("Rizvanchik_", ))
                await db.commit()
                return "Rizvanchik_"
            return result[0]

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
        await db.commit()

async def add_main_admin(user_id: int, username: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET class = ? WHERE user_id = ?", ('main_admin',user_id))
        await db.commit()

async def add_user(user_id: int, username: str) -> None:
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''INSERT OR IGNORE INTO users (user_id, username, broadcast) VALUES (?,?)''', (user_id, username, 1))
        await db.commit()
# ПОИСК
# ПОИСК
async def search_user(user_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT 1 FROM users WHERE class = ? AND user_id = ?",
            ('user', str(user_id))
        ) as cursor:
            result = await cursor.fetchone()
            if result:
                return result
            else:
                return False

async def search_admin(user_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT 1 FROM users WHERE class = ? AND user_id = ?",
            ('admin', str(user_id))
        ) as cursor:
            result = await cursor.fetchone()
            if result:
                return True
            else:
                return False

async def search_main_admin(user_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT user_id FROM users WHERE class = ? AND user_id = ?",
            ('main_admin', str(user_id))
        ) as cursor:
            result = await cursor.fetchone()
            if result:
                return True
            else:
                return False



