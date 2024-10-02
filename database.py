import sqlite3
from datetime import datetime

def create_connection():
    return sqlite3.connect('subscriptions.db')

def create_db():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscriptions (
        user_id INTEGER PRIMARY KEY,
        expiration_date TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS whitelist (
        user_id INTEGER PRIMARY KEY
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    )
    ''')
    
    conn.commit()
    conn.close()

def add_to_db(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO users (user_id)
    VALUES (?)
    ON CONFLICT(user_id) DO NOTHING
    ''', (user_id,))
    
    conn.commit()
    conn.close()

def check_subscription(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT expiration_date FROM subscriptions WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        expiration_date = datetime.fromisoformat(result[0])
        return expiration_date > datetime.now()
    return False

def add_subscription(user_id, expiration_date):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO subscriptions (user_id, expiration_date)
    VALUES (?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
    expiration_date=excluded.expiration_date
    ''', (user_id, expiration_date.isoformat()))
    conn.commit()
    conn.close()

def is_whitelisted(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM whitelist WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_to_whitelist(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO whitelist (user_id)
    VALUES (?)
    ON CONFLICT(user_id) DO NOTHING
    ''', (user_id,))
    conn.commit()
    conn.close()

def remove_subscription(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM subscriptions WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def remove_from_whitelist(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM whitelist WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_all_users_from_db():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM subscriptions')
    users_subscriptions = cursor.fetchall()

    cursor.execute('SELECT user_id FROM whitelist')
    users_whitelist = cursor.fetchall()

    cursor.execute('SELECT user_id FROM users')
    all_users_db = cursor.fetchall()

    all_users = {user[0] for user in users_subscriptions + users_whitelist + all_users_db}
    conn.close()

    return [{'id': user_id, 'name': f'User {user_id}'} for user_id in all_users]