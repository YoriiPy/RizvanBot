import aiosqlite

DB_NAME = ("database.db")
async def main():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS streams(
                                channel_id TEXT,
                                last_stream_id TEXT
                                is_live BOOLEAN,
                                last_title TEXT, 
                        ''')
        await db.execute('''CREATE TABLE IF NOT EXISTS users(
                                user_id TEXT,
                                username TEXT,
                                broadcast BOOLEAN,
                                class TEXT DEFAULT "user" 
                        ''')
