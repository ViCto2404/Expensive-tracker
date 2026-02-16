"""Expense Tracker Application - Main Entry Point

This module serves as the entry point for the Expense Tracker application.
It initializes the database manager, expense analyzer, and GUI components,
and launches the main application window.
"""

from database.db_manager import DatabaseManager
from logic.analyzer import ExpenseAnalyzer
from gui.main_window import MainWindow

def main():
    """Initialize and run the Expense Tracker application.
    
    Creates instances of:
    - DatabaseManager: Handles all database operations
    - ExpenseAnalyzer: Performs expense analysis and calculations
    - MainWindow: Renders the GUI interface
    
    Then launches the GUI main loop.
    """
    # Initialize the database manager
    db = DatabaseManager()

    # Create the analyzer with database reference
    analyzer = ExpenseAnalyzer(db)

    # Initialize the main GUI window with database and analyzer
    app = MainWindow(db, analyzer)

    # Start the application
    app.run()

if __name__ == "__main__":
    main()