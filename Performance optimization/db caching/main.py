import sqlite3
import redis
import hashlib
import json
import logging
from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(
    level = logging.INFO,
    format="[%(asctime)s] - (line %(lineno)d) - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

logging.info("FastAPI INstance created")
app = FastAPI()

logging.info("Redis client created")
redis_client = redis.Redis(host='localhost',port=6379, db=0)


def get_db_connection():
    logging.info("DB Connection.....")
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    logging.info("User Table is created")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   age INTEGER)
""")
    logging.info("Inserted data point into user table")
    cursor.execute("INSERT INTO users (id, name, age) VALUES (1, 'Michel',45)")
    cursor.execute("INSERT INTO users (id, name, age) VALUES (2, 'John',40)")
    cursor.execute("INSERT INTO users (id, name, age) VALUES (3, 'Mohit',34)")
    logging.info("Data commited !")
    conn.commit()
    logging.info("Connection closed..")
    conn.close()


init_db()


class UserQuery(BaseModel):
    user_id :int

def make_cache_key(user_id:int):
    raw = f"user: {user_id}"
    return hashlib.sha256(raw.encode()).hexdigest()


logging.info("FastApi EndPoint.......")
@app.post('/get-user')
def get_user(query:UserQuery):
    cache_key = make_cache_key(query.user_id)
    logging.info(f"cached key : {cache_key}")

    cached_data = redis_client.get(cache_key)
    logging.info(f"cached data : {cached_data}")

    if cached_data: 
        print("Serving from Redis Cache!")
        return json.loads(cached_data)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM users WHERE id = ? """,(query.user_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {'message':'user not found.'}
    
    result  =  {'if':row['id'],'name':row['name'],'age':row['age']}
    redis_client.setex(cache_key, 3600, json.dumps(result))
    print('Fetched from DB and Cached!')

    return result