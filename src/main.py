from database.db_manager import DatabaseManager

db = DatabaseManager()

print("Guardando gasto")
db.add_expense(15.50, "Almuerzo", '2026-01-08', "Pizza")

gastos = db.fetch_all_expenses()
print("Gastos encontrados en la base de datos:")
for g in gastos:
    print(g)