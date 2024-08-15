import sqlite3

# Укажите путь к вашему файлу базы данных
db_path = 'db.sqlite3'

# Подключение к базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts_questprogress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    quest_id INTEGER NOT NULL,
    is_completed BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES accounts_customuser (id),
    FOREIGN KEY (quest_id) REFERENCES accounts_quest (id),
    UNIQUE (user_id, quest_id)
);
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Table created successfully.")
