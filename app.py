from flask import Flask, request, jsonify, render_template_string, escape
import sqlite3
import hashlib
import os
import re
import bcrypt

app = Flask(__name__)

# Bug 1: SQL Injection vulnerability - FIXED
def get_user_by_id(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # FIXED: Use parameterized query to prevent SQL injection
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Bug 2: Insecure password hashing - FIXED

def hash_password(password):
    # FIXED: Use bcrypt for secure password hashing
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed_password):
    # Helper function to verify passwords
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Bug 3: XSS vulnerability - FIXED

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # FIXED: Properly escape user input to prevent XSS
    escaped_query = escape(query)
    template = f"""
    <html>
        <head><title>Search Results</title></head>
        <body>
            <h1>Search Results for: {escaped_query}</h1>
            <p>No results found for your query.</p>
        </body>
    </html>
    """
    return render_template_string(template)

# Bug 4: Race condition in file operations
def append_to_log(message):
    # VULNERABLE: Race condition when multiple processes write to same file
    with open('app.log', 'a') as f:
        f.write(message + '\n')

# Bug 5: Memory leak in list operations
def process_data(data_list):
    # VULNERABLE: Creates infinite list growth
    result = []
    for item in data_list:
        result.append(item)
        result.extend(data_list)  # This causes exponential growth
    return result

# Bug 6: Insecure random number generation
import random
def generate_token():
    # VULNERABLE: Using predictable random number generator
    return random.randint(1000, 9999)

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify({'id': user[0], 'name': user[1], 'email': user[2]})
    return jsonify({'error': 'User not found'}), 404

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Hash password using insecure method
    hashed_password = hash_password(password)
    
    # Store user (simplified)
    append_to_log(f"New user registered: {username}")
    return jsonify({'message': 'User registered successfully'})

@app.route('/')
def index():
    return '''
    <html>
        <head><title>Buggy App</title></head>
        <body>
            <h1>Welcome to the Buggy App</h1>
            <p>This app contains several intentional bugs for demonstration.</p>
            <a href="/search?q=test">Test Search</a>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)