from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/search')
def search_users():
    query = request.args.get('q', '')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Vulnerable: taint từ user input chảy vào query string (format hoặc %)
    sql = "SELECT * FROM users WHERE name LIKE '%{}%' OR email = '{}'".format(query, query)
    # Hoặc: sql = f"SELECT * FROM users WHERE name LIKE '%{query}%'"
    
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return str(results)