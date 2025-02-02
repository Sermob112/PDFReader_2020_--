import camelot
import pandas as pd

# Укажите путь к вашему PDF файлу
pdf_path = 'HHI.pdf'

# Извлечение таблиц из PDF
tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')

# Создание Excel файла
with pd.ExcelWriter('output.xlsx') as writer:
    for i, table in enumerate(tables):
        # Преобразование таблицы в DataFrame
        df = table.df
        # Сохранение каждой таблицы на отдельный лист
        df.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)

print(f"Таблицы сохранены в output.xlsx")


