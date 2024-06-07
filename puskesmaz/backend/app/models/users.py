import sqlite3
from flask import current_app
from app.utils import hash_password

def connect_to_db():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    return conn

def create_users_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("Users table created successfully")
    except Exception as e:
        print(f"Users table creation failed: {e}")
    finally:
        conn.close()

def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        hashed_password = hash_password(user['password'])
        cur.execute('''INSERT INTO users (name, email, password, phone, address, country) VALUES (?, ?, ?, ?, ?, ?)''', 
                    (user['name'], user['email'], hashed_password, user['phone'], user['address'], user['country']))
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
    return inserted_user

def get_user_by_email(email):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cur.fetchone()
        if row:
            user["user_id"] = row["user_id"]
            user["name"] = row["name"]
            user["email"] = row["email"]
            user["password"] = row["password"]
            user["phone"] = row["phone"]
            user["address"] = row["address"]
            user["country"] = row["country"]
    except Exception as e:
        print(e)
        user = {}
    return user


def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        for i in rows:
            user = {}
            user["user_id"] = i["user_id"]
            user["name"] = i["name"]
            user["email"] = i["email"]
            user["phone"] = i["phone"]
            user["address"] = i["address"]
            user["country"] = i["country"]
            users.append(user)
    except Exception as e:
        print(e)
        users = []
    return users

def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            user["user_id"] = row["user_id"]
            user["name"] = row["name"]
            user["email"] = row["email"]
            user["phone"] = row["phone"]
            user["address"] = row["address"]
            user["country"] = row["country"]
    except Exception as e:
        print(e)
        user = {}
    return user

def update_user(user):
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?''',  
                    (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"]))
        conn.commit()
        updated_user = get_user_by_id(user["user_id"])
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
    return updated_user

def delete_user(user_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute('''DELETE from users WHERE user_id = ?''', (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception as e:
        print(e)
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()
    return message
