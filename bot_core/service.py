import sqlite3
import logging
from bot_core.coordinates import Coordinates
from datetime import datetime

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

async def insert_data_into_db(location: Coordinates, weather: str, wind: str, sun_time: str, user_id: int):
    connection_to_db = await create_connection(logging)
    cursor = await create_table(connection_to_db, logging)
    cursor.execute("""insert into users values(?, ?, ?, ?, ?, ?, ?);""", (user_id, location.latitude, location.longitude, weather, wind, sun_time, datetime.now()))
    connection_to_db.commit()
    
async def take_update(user_id: int):
    print(user_id)
    connection_to_db = await create_connection(logging)
    cursor = await create_table(connection_to_db, logging)
    cursor.execute('select * from users where userid is 759867694;')
    row = cursor.fetchall()
    print(row)
    return 100
