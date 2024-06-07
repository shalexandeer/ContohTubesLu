import sqlite3
from flask import current_app

def connect_to_db():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    return conn

def create_medicine_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS medicine (
                medicine_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                manufacturer TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                price REAL NOT NULL
            );
        ''')
        conn.commit()
        print("Medicine table created successfully")
    except Exception as e:
        print(f"Medicine table creation failed: {e}")
    finally:
        conn.close()

def insert_medicine(medicine):
    inserted_medicine = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO medicine (name, description, price) VALUES (?, ?, ?)''', 
                    (medicine['name'], medicine['description'], medicine['price']))
        conn.commit()
        inserted_medicine = get_medicine_by_id(cur.lastrowid)
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
    return inserted_medicine

def get_medicines():
    medicines = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicine")
        rows = cur.fetchall()

        for i in rows:
            medicine = {}
            medicine["medicine_id"] = i["medicine_id"]
            medicine["name"] = i["name"]
            medicine["description"] = i["description"]
            medicine["price"] = i["price"]
            medicines.append(medicine)
    except Exception as e:
        print(e)
        medicines = []
    return medicines

def get_medicine_by_id(medicine_id):
    medicine = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicine WHERE medicine_id = ?", (medicine_id,))
        row = cur.fetchone()
        if row:
            medicine["medicine_id"] = row["medicine_id"]
            medicine["name"] = row["name"]
            medicine["description"] = row["description"]
            medicine["price"] = row["price"]
    except Exception as e:
        print(e)
        medicine = {}
    return medicine

def update_medicine(medicine):
    updated_medicine = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE medicine SET name = ?, description = ?, price = ? WHERE medicine_id = ?''',  
                    (medicine["name"], medicine["description"], medicine["price"], medicine["medicine_id"]))
        conn.commit()
        updated_medicine = get_medicine_by_id(medicine["medicine_id"])
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
    return updated_medicine

def delete_medicine(medicine_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute('''DELETE from medicine WHERE medicine_id = ?''', (medicine_id,))
        conn.commit()
        message["status"] = "Medicine deleted successfully"
    except Exception as e:
        print(e)
        conn.rollback()
        message["status"] = "Cannot delete medicine"
    finally:
        conn.close()
    return message
