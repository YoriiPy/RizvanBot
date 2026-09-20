

import aiosqlite

DB_NAME = ("database.db")
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS streams(
                                channel_name TEXT PRIMARY KEY,
                                channel_id TEXT NOT NULL
                                )
                        ''')
        await db.commit()

        await db.execute('''CREATE TABLE IF NOT EXISTS users(                    
                                user_id TEXT PRIMARY KEY,
                                username TEXT ,
                                broadcast INTEGER DEFAULT 1,
                                class TEXT DEFAULT 'user')
                        ''')
        await db.commit()
