import camelot
import pandas as pd

# Укажите путь к вашему PDF-файлу
pdf_path = "ReaderMannCatalog\\MAN2024.pdf"

# Извлечение таблиц из PDF
tables = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")

# Сохранение каждой таблицы в отдельный лист Excel
with pd.ExcelWriter("ReaderMannCatalog\\Mannoutput.xlsx") as writer:
    for i, table in enumerate(tables):
        table.df.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)

print(f"Извлечено {tables.n} таблиц. Результат сохранен в output.xlsx.")