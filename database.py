import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "kontanta.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Таблица вакансий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                requirements TEXT,
                salary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Таблица заявок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                vacancy_id INTEGER NOT NULL,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                experience TEXT,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (vacancy_id) REFERENCES vacancies (id)
            )
        ''')

        # Таблица подписок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        # Таблица сохранённых заявок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                vacancy_id INTEGER NOT NULL,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (vacancy_id) REFERENCES vacancies (id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_user(self, user_id: int, first_name: str, last_name: str = "", username: str = ""):
        """Добавить или обновить пользователя"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, first_name, last_name, username)
            VALUES (?, ?, ?, ?)
        ''', (user_id, first_name, last_name, username))
        
        conn.commit()
        conn.close()

    def get_vacancies(self, category: Optional[str] = None) -> List[Dict]:
        """Получить вакансии, опционально по категории"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if category:
            cursor.execute('SELECT * FROM vacancies WHERE category = ? ORDER BY created_at DESC', (category,))
        else:
            cursor.execute('SELECT * FROM vacancies ORDER BY created_at DESC')

        vacancies = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return vacancies

    def get_vacancy_by_id(self, vacancy_id: int) -> Optional[Dict]:
        """Получить вакансию по ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM vacancies WHERE id = ?', (vacancy_id,))
        vacancy = dict(cursor.fetchone()) if cursor.fetchone() else None
        
        conn.close()
        return vacancy

    def add_vacancy(self, title: str, category: str, description: str, requirements: str = "", salary: str = ""):
        """Добавить вакансию"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO vacancies (title, category, description, requirements, salary)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, category, description, requirements, salary))

        conn.commit()
        vacancy_id = cursor.lastrowid
        conn.close()
        return vacancy_id

    def add_application(self, user_id: int, vacancy_id: int, full_name: str, phone: str, email: str, experience: str = ""):
        """Добавить заявку"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO applications (user_id, vacancy_id, full_name, phone, email, experience)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, vacancy_id, full_name, phone, email, experience))

        conn.commit()
        application_id = cursor.lastrowid
        conn.close()
        return application_id

    def add_subscription(self, user_id: int, category: str = None):
        """Добавить подписку на категорию"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO subscriptions (user_id, category)
            VALUES (?, ?)
        ''', (user_id, category))

        conn.commit()
        conn.close()

    def save_draft(self, user_id: int, vacancy_id: int, data: str):
        """Сохранить черновик заявки"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO drafts (user_id, vacancy_id, data)
            VALUES (?, ?, ?)
        ''', (user_id, vacancy_id, data))

        conn.commit()
        conn.close()

    def get_draft(self, user_id: int, vacancy_id: int) -> Optional[str]:
        """Получить черновик заявки"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT data FROM drafts WHERE user_id = ? AND vacancy_id = ?', (user_id, vacancy_id))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None
