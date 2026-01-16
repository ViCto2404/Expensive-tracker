import sqlite3
import os
from sqlite3 import Error
from typing import List, Tuple, Optional
from logger import logger

class DatabaseManager:

    def __init__(self, db_path: str = None):
        # 1. CÁLCULO DE RUTA ABSOLUTA (Independiente de la terminal)
        if db_path is None:
            # Obtenemos la ruta de este archivo: .../src/database/db_manager.py
            current_file = os.path.abspath(__file__)
            # Subimos 3 niveles para llegar a la raíz: Expensive-tracker/
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
            self.db_path = os.path.join(project_root, 'data', 'expenses.db')
        else:
            self.db_path = os.path.abspath(db_path)

        # 2. VERIFICACIÓN DE CARPETA (Fuerza la creación si algo falla)
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir, exist_ok=True)
                logger.info(f"Carpeta creada/verificada en: {db_dir}")
            except Exception as e:
                print(f"🚨 ERROR CRÍTICO: No se pudo crear la carpeta {db_dir}. {e}")

        print(f"🔍 Intentando conectar a: {self.db_path}")
        self.create_table()

    def _get_connection(self):
        try:
            # check_same_thread=False es útil para aplicaciones GUI futuras
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            return conn
        except Error as e:
            # Imprimimos en consola también para que no se pierda en el log
            print(f"❌ Error de SQLite: {e}")
            logger.error(f"Error connecting to database: {e}")
            return None
        
    def create_table(self) -> None:
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
        
        # 3. PROTECCIÓN CONTRA EL ERROR NoneType
        if conn is not None:
            try:
                with conn:
                    conn.execute(query)
                logger.info("Base de datos y tabla listas.")
            except Error as e:
                logger.error(f"Error al ejecutar query: {e}")
            finally:
                conn.close()
        else:
            # Esto te dirá exactamente por qué falló la conexión antes del crash
            print("🚨 No se pudo iniciar la tabla: La conexión es None.")

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