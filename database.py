import sqlite3

def create_database():
    conn = sqlite3.connect('nutrition.db')
    c = conn.cursor() # c - cursor

    # Таблица пользователей
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE,
                 age INTEGER,
                 gender TEXT,
                 weight REAL,
                 height REAL,
                 activity REAL,
                 goal TEXT,
                 calories_norm REAL)''')

    # Таблица продуктов
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT UNIQUE,
                 calories REAL,
                 proteins REAL,
                 fats REAL,
                 carbs REAL)''')

    # Таблица блюд
    c.execute('''CREATE TABLE IF NOT EXISTS dishes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT UNIQUE,
                 category TEXT CHECK(category IN ('Завтрак', 'Обед', 'Ужин')))''')

    # Таблица состава блюд
    c.execute('''CREATE TABLE IF NOT EXISTS dish_composition
                 (dish_id INTEGER,
                 product_id INTEGER,
                 grams REAL,
                 FOREIGN KEY(dish_id) REFERENCES dishes(id),
                 FOREIGN KEY(product_id) REFERENCES products(id))''')

    conn.commit()
    conn.close()


