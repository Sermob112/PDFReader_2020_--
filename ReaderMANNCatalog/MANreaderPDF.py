import fitz  # PyMuPDF
import camelot
import tabula

def pdf_to_text(pdf_path, txt_path):
    # Открываем PDF файл
    pdf_document = fitz.open(pdf_path)
    
    # Открываем TXT файл для записи
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        # Проходим по каждой странице PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)  # Загружаем страницу
            text = page.get_text()  # Извлекаем текст
            txt_file.write(text)  # Записываем текст в TXT файл
    
    print(f"Текст успешно извлечен и сохранен в {txt_path}")

# Укажите путь к вашему PDF файлу и путь для сохранения TXT файла
pdf_path = "ReaderMANNCatalog\\MAN2024.pdf"
txt_path = "ReaderMANNCatalog\\output.txt"

# Вызываем функцию для извлечения текста
# pdf_to_text(pdf_path, txt_path)


tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

# Сохраняем таблицы в CSV файлы
for i, table in enumerate(tables):
    table.to_csv(f"ReaderMANNCatalog\\Tables\\table_{i}.csv")  # Сохраняем каждую таблицу в отдельный CSV файл
    print(f"Таблица {i} сохранена в table_{i}.csv")

# Выводим информацию о таблицах
print(f"Найдено {tables.n} таблиц.")