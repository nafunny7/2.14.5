import sqlite3

connection = sqlite3.connect("db.db")
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NON NULL,
    description TEXT,
    price INTEGER NON NULL)
    ''')
    connection.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NON NULL,
    email TEXT NON NULL,
    age INTEGER NON NULL,
    balance INTEGER NON NULL)
    ''')
    connection.commit()


initiate_db()


def get_all_products():
    connection = sqlite3.connect('product_data1.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, description, price FROM Products")
    elements = cursor.fetchall()
    connection.commit()
    return elements


def add_user(username, email, age):
    connection = sqlite3.connect('product_data1.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
                   (username, email, age, 1000))
    connection.commit()


def is_included(username):
    connection = sqlite3.connect('product_data1.db')
    cursor = connection.cursor()
    check_user = cursor.execute("SELECT id FROM Users WHERE username =   ?", (username,)).fetchone()
    if check_user is None:
        connection.commit()
        return False
    else:
        connection.commit()
        return True
