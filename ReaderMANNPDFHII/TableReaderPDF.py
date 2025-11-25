import camelot
import pandas as pd


pdf_path = 'HHI.pdf'

tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')


with pd.ExcelWriter('output.xlsx') as writer:
    for i, table in enumerate(tables):

        df = table.df

        df.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)

print(f"Таблицы сохранены в output.xlsx")


