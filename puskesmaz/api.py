import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

def connect_to_db():
    conn = sqlite3.connect("database.db")
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("User table created successfully")
    except Exception as e:
        print(f"User table creation failed: {e}")
    finally:
        conn.close()

def make_response(status, message, data):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response)

def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)''', 
                    (user['name'], user['email'], user['phone'], user['address'], user['country']))
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()
    return inserted_user

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

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins":"*"}})

@app.route("/api/users", methods=["GET"])
def api_get_users():
    users = get_users()
    return make_response(200, "Users retrieved successfully", users)

@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return make_response(200, "User retrieved successfully", user)
    else:
        return make_response(404, "User not found", {})

@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    user = request.get_json()
    inserted_user = insert_user(user)
    if inserted_user:
        return make_response(201, "User added successfully", inserted_user)
    else:
        return make_response(400, "Error adding user", {})

@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    user = request.get_json()
    updated_user = update_user(user)
    if updated_user:
        return make_response(200, "User updated successfully", updated_user)
    else:
        return make_response(400, "Error updating user", {})

@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    result = delete_user(user_id)
    if result["status"] == "User deleted successfully":
        return make_response(200, result["status"], {})
    else:
        return make_response(400, result["status"], {})

if __name__ == '__main__':
    create_db_table()  # Ensure the table is created before starting the app
    app.run()
