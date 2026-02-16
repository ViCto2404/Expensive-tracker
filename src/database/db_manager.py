"""Database Management Module

This module handles all database operations for the Expense Tracker application.
It manages SQLite database connections, table creation, and CRUD operations
for expense records.
"""

import sqlite3
import os
from sqlite3 import Error
from typing import List, Tuple, Optional
from logger import logger

class DatabaseManager:
    """Manages SQLite database operations for expense tracking.
    
    Handles database initialization, table creation, and all CRUD operations
    for expense records. Automatically creates the data directory and database
    file if they don't exist.
    """

    def __init__(self, db_path: str = None):
        """Initialize DatabaseManager and create database if needed.
        
        Args:
            db_path (str, optional): Path to the SQLite database file.
                    If None, defaults to 'data/expenses.db' relative to project root.
        """
        # Calculate the database path based on project structure
        if db_path is None:
            # Get the absolute path of this file: .../src/database/db_manager.py
            current_file = os.path.abspath(__file__)
            # Navigate up 3 levels to reach project root: Expensive-tracker/
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
            self.db_path = os.path.join(project_root, 'data', 'expenses.db')
        else:
            # Use the provided path as absolute path
            self.db_path = os.path.abspath(db_path)

        # Ensure the database directory exists (create if necessary)
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir, exist_ok=True)
                logger.info(f"Database directory created/verified at: {db_dir}")
            except Exception as e:
                print(f"CRITICAL ERROR: Could not create directory {db_dir}. {e}")

        print(f"Attempting to connect to database: {self.db_path}")
        # Initialize the database table structure
        self.create_table()

    def _get_connection(self):
        """Establish a connection to the SQLite database.
        
        Returns:
            sqlite3.Connection: Database connection object, or None if connection fails.
        """
        try:
            # check_same_thread=False allows GUI applications to access the database
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            return conn
        except Error as e:
            # Log to both console and file for visibility
            print(f"SQLite Error: {e}")
            logger.error(f"Error connecting to database: {e}")
            return None
        
    def create_table(self) -> None:
        """Create the expenses table if it does not already exist.
        
        The expenses table stores:
        - id: Auto-incrementing primary key
        - amount: Expense amount (decimal)
        - category: Category of the expense
        - date: Date and time of the expense
        - description: Optional description of the expense
        """
        # SQL query to create the expenses table
        query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        );
        """
        conn = self._get_connection()
        
        # Verify connection is successful before executing query
        if conn is not None:
            try:
                with conn:
                    conn.execute(query)
                logger.info("Database and table initialized successfully.")
            except Error as e:
                logger.error(f"Error executing query: {e}")
            finally:
                conn.close()
        else:
            # Connection failed - log the critical error
            print("CRITICAL ERROR: Could not initialize table. Connection is None.")

    def add_expense(self, amount: float, category: str, date: str, description: Optional[str] = None) -> bool:
        """Add a new expense record to the database.
        
        Args:
            amount (float): The expense amount
            category (str): The expense category (e.g., 'Food', 'Transport', etc.)
            date (str): The date and time of the expense (format: YYYY-MM-DD HH:MM:SS)
            description (str, optional): Additional description or notes about the expense
            
        Returns:
            bool: True if expense was added successfully, False otherwise
        """
        # SQL query to insert a new expense record
        query = 'INSERT INTO expenses (amount, category, date, description) VALUES (?,?,?,?)'

        try:
            with self._get_connection() as conn:
                if conn:
                    conn.execute(query, (amount, category, date, description))
                    logger.info(f"Expense added: {amount} in {category} on {date}")
                    return True
        except Error as e:
            logger.error(f"Error adding expense: {e}")
            return False
        return False
    
    def fetch_all_expenses(self) -> list[Tuple]:
        """Retrieve all expenses from the database, ordered by date (newest first).
        
        Returns:
            list[Tuple]: List of tuples containing all expenses (id, amount, category, date, description)
                        Returns empty list if no expenses exist or if an error occurs
        """
        # SQL query to fetch all expenses ordered by date in descending order
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