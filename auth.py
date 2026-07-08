import sqlite3

from database import connect_db
from passlib.context import CryptContext

pwd_context =  CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def create_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
        INSERT INTO users(username, password) 
        VALUES (?,?)
    """, (username, hashed_password))

    conn.commit()
    conn.close()

def delete_user(id):
    conn= connect_db()
    cursor= conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE id = ?
        """, (id,)
    )

    conn.commit()
    conn.close()

def hash_password(password):
    return pwd_context.hash(password)

def get_user(username):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * 
        FROM users 
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()
    conn.close()
    return user

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)