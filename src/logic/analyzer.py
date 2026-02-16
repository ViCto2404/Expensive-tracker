"""Expense Analysis Module

This module provides analytical functions for the Expense Tracker.
It processes expense data and generates insights such as totals by category,
overall balance, and other statistical information.
"""

import pandas as pd
from database.db_manager import DatabaseManager
from logger import logger

class ExpenseAnalyzer:
    """Analyzes expense data and generates analytical reports.
    
    Processes data from the database and performs calculations to provide
    insights into spending patterns by category and overall expenses.
    """

    def __init__(self, db_manager: DatabaseManager):
        """Initialize the ExpenseAnalyzer with a database manager.
        
        Args:
            db_manager (DatabaseManager): Instance of DatabaseManager for data access
        """
        self.db = db_manager

    def get_all_as_dataframe(self) -> pd.DataFrame:
        """Fetch all expenses and convert them to a pandas DataFrame.
        
        Automatically converts the 'amount' column to numeric type for calculations.
        
        Returns:
            pd.DataFrame: DataFrame with columns: id, amount, category, date, description
                         Returns empty DataFrame if no expenses exist
        """
        # Fetch all expense records from the database
        raw_data = self.db.fetch_all_expenses()
        # Define column names for the DataFrame
        columns = ['id', 'amount', 'category', 'date', 'description']

        # Create DataFrame from raw data
        df = pd.DataFrame(raw_data, columns=columns)

        # Ensure amount column is numeric for calculations
        if not df.empty:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

        return df
    
    def get_total_balance(self) -> float:
        """Calculate the total balance of all expenses.
        
        Returns:
            float: Sum of all expense amounts. Returns 0.0 if no expenses exist.
        """
        # Get all expenses as a DataFrame
        df = self.get_all_as_dataframe()
        # Return 0 if no expenses recorded yet
        if df.empty:
            return 0.0
        # Return the sum of all amounts
        return float(df['amount'].sum())
    
    def get_category_totals(self):
        """Analyze total expenses grouped by category.
        
        Returns:
            pd.Series: Series with category names as index and total amounts as values
                      Returns empty Series if no expenses exist
        """
        # Get all expenses as a DataFrame
        df = self.get_all_as_dataframe()
        # Return empty Series if no expenses recorded yet
        if df.empty:
            return pd.Series(dtype=float)
        # Group expenses by category and sum the amounts
        return df.groupby('category')['amount'].sum()
