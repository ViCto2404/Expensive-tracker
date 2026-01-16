import sqlite3
import os
from sqlite3 import Error
from typing import List, Tuple, Optional
from src.logger import logger

class DatabaseManager:

    def __init__(self, db_path: str='None'):
        
        if db_path is None:
            file_path = os.path.abspath(__file__)
            root = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
            self.db_path = os.path.join(root, 'data', 'expenses.db')
        else:
            self.db_path = db_path

        self._ensure_data_folder_exists()
        self.create_table()
    
    def _ensure_data_folder_exists(self):
        folder = os.path.dirname(self.db_path)
        if not os.path.exists(folder):
            os.makedirs(folder)
            logger.info(f'Created data folder at {folder}')

    
    def _get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except Error as e:
            logger.error(f"Error connecting to database: {e}")
            return None
        
    def create_table(self) -> None:

        query = """

        CREATE TABLE IF NO EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        );
        """

        try:
            with self._get_connection() as conn:
                conn.execute(query)
                logger.info("Expenses database created or already exists.")
        except Error as e:
            logger.error(f"Error creating database: {e}")

    def add_expense(self, amount: float, category: str, date: str, description: Optional[str] = None) -> bool:

        query = 'INSERT INTO expenses (amount, category, date, description) VALUES (?,?,?,?)'

        try:
            with self._get_connection() as conn:
                if conn:
                    conn.execute(query, (amount, category, date, description))
                    logger.info(f"added expense: {amount} in {category} on {date}")
                    return True
        except Error as e:
            logger.error("Error adding expense: {e}")
            return False
        return False
    
    def fetch_all_expenses(self) -> list[Tuple]:

        query = 'SELECT * FROM expenses ORDER BY date DESC'

        try:
            with self._get_connection() as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    return rows
        except Error as e:
            logger.error(f'Error fetching expenses: {e}')
            return []
        return []