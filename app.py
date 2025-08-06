from flask import Flask, request, jsonify, render_template_string
import sqlite3
import hashlib
import os
import re

app = Flask(__name__)

# Bug 1: SQL Injection vulnerability - FIXED
def get_user_by_id(user_id):
    # FIXED: Use parameterized query and context manager
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        return user

# Bug 2: Insecure password hashing - FIXED
def hash_password(password):
    # FIXED: Use bcrypt for secure password hashing
    import bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed_password):
    # FIXED: Add password verification function
    import bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Bug 3: Inefficient database connection handling - FIXED
def get_all_users():
    # FIXED: Use context manager to ensure proper connection handling
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users

@app.route('/')
def index():
    return render_template_string('''
        <h1>User Management System</h1>
        <form action="/user" method="GET">
            <input type="text" name="user_id" placeholder="Enter user ID">
            <button type="submit">Get User</button>
        </form>
        <form action="/users" method="GET">
            <button type="submit">Get All Users</button>
        </form>
    ''')

@app.route('/user')
def get_user():
    user_id = request.args.get('user_id')
    if user_id:
        user = get_user_by_id(user_id)
        return jsonify(user if user else {'error': 'User not found'})
    return jsonify({'error': 'No user ID provided'})

@app.route('/users')
def list_users():
    users = get_all_users()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)