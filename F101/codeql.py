# Vulnerable: SQL Injection qua string concatenation
from django.db import connection

def get_user(request, username):
    cursor = connection.cursor()
    # Không sanitize input → attacker có thể inject: ' OR '1'='1
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()