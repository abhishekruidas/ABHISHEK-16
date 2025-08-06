import sqlite3

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Insert some sample data
    sample_users = [
        (1, 'admin', 'admin@example.com', '5f4dcc3b5aa765d61d8327deb882cf99'),  # password: password
        (2, 'user1', 'user1@example.com', 'e10adc3949ba59abbe56e057f20f883e'),  # password: 123456
        (3, 'user2', 'user2@example.com', 'd8578edf8458ce06fbc5bb76a58c5ca4')   # password: qwerty
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)', sample_users)
    conn.commit()
    conn.close()
    
    print("Database setup complete!")

if __name__ == '__main__':
    setup_database()