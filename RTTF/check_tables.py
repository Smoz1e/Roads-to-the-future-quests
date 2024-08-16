import sqlite3

# Укажите путь к вашему файлу базы данных
db_path = 'db.sqlite3'

# Подключение к базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Запрос всех таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Печать списка таблиц
print("Tables in database:", tables)

# Закрытие соединения
conn.close()
