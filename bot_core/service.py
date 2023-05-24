import sqlite3
import aiohttp, asyncio
import logging

async def db_init(logging: logging) -> None:
    connection_to_db = await create_connection(logging)
    
    if not connection_to_db == None:
        await create_table(connection_to_db, logging)

async def create_connection(logging: logging) -> sqlite3.Connection|None:
    connection_to_db = None
    try:
        connection_to_db = sqlite3.connect('sql.db')
        return connection_to_db
    except ConnectionError as e:
        logging.info(e)
    
    return connection_to_db

async def create_table(connection_to_db: sqlite3.Connection, logging: logging) -> sqlite3.Cursor|None:
    cursor = None
    try:
        cursor = connection_to_db.cursor()

        cursor.execute("""create table if not exists users(
            userid INT PRIMARY KEY,
            user_latitude REAL not null,
            user_longitude REAL  not null,
            current_weather TEXT  not null,
            current_wind TEXT  not null,
            current_sun_time TEXT not null,
            weather_time_request DATETIME);
            """)

        connection_to_db.commit()
    except BaseException as e:
        logging.info(e)
    
    return cursor

