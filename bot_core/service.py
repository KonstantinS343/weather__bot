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
            weather_time_request DATETIME);
            """)

        connection_to_db.commit()
    except BaseException as e:
        logging.info(e)
    
    return cursor

async def insert_or_update_data_into_db(location: Coordinates, weather: str, user_id: int):
    connection_to_db = await create_connection(logging)
    cursor = await create_table(connection_to_db, logging)
    request = f'select * from users where userid is {user_id}'
    cursor.execute(request)
    row = cursor.fetchall()
    if not row:
        cursor.execute("""insert into users values(?, ?, ?, ?, ?);""", (user_id, location.latitude, location.longitude, weather, datetime.now()))
    else:
        cursor.execute("""update users set user_latitude=?, user_longitude=?, current_weather=?, weather_time_request=?""", (location.latitude, location.longitude, weather, datetime.now()))
    connection_to_db.commit()
    
async def take_update(user_id: int) -> datetime:
    connection_to_db = await create_connection(logging)
    cursor = await create_table(connection_to_db, logging)
    request = f'select * from users where userid is {user_id}'
    cursor.execute(request)
    row = cursor.fetchall()
    logging.info(row)
    time = datetime.strptime(row[0][-1], '%Y-%m-%d %H:%M:%S.%f')
    return time

async def get_user_location(user_id: int) -> Coordinates|None:
    connection_to_db = await create_connection(logging)
    cursor = await create_table(connection_to_db, logging)
    request = f'select * from users where userid is {user_id}'
    cursor.execute(request)
    row = cursor.fetchall()
    if row:
        return Coordinates(latitude=row[0][1], longitude=row[0][2])
    else:
        return None

async def get_weather_db(user_id: int) -> Coordinates|None:
    connection_to_db = await create_connection(logging)
    cursor = await create_table(connection_to_db, logging)
    request = f'select * from users where userid is {user_id}'
    cursor.execute(request)
    row = cursor.fetchall()
    return row[0][3]