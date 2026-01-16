import pandas as pd
from database.db_manager import DatabaseManager
from logger import logger

class ExpenseAnalyzer:

    def _init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def get_all_as_dataframe(self) -> pd.DataFrame:
        raw_data = self.db.fetch_all_expenses()
        columns = ['id', 'amount', 'category', 'date', 'description']

        df = pd.DataFrame(raw_data, columns=columns)

        if not df.empty:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

        return df
    
    def get_total_balance(self) -> float:
        df = self.get_all_as_dataframe()
        if df.empty:
            return 0.0
        return float(df['amount'].sum())
    
    def get_category_totals(self):
        df = self.get_all_as_dataframe()
        if df.empty:
            return pd.Series(dtype=float)
        return df.groupby('category')['amount'].sum()
