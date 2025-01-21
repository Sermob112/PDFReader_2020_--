import fitz

def pdf_to_txt_with_mupdf(pdf_path, txt_path):
    doc = fitz.open(pdf_path)
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for page in doc:
            # Получаем словарь с информацией о форматировании
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            font = span["font"]
                            size = span["size"]
                            text = span["text"]
                            
                            # Проверяем, соответствует ли текст формату заголовка
                            if ('Arial-Black' in font and 
                                abs(size - 22) < 1):  # размер около 22pt
                                txt_file.write(f"ЗАГОЛОВОК: {text}\n")
                            else:
                                txt_file.write(text)
                        txt_file.write("\n")

# Установка библиотеки:
# pip install PyMuPDF
pdf_file_path = 'Test.pdf'
txt_file_path = 'output2.txt'
# Использование
pdf_to_txt_with_mupdf(pdf_file_path, txt_file_path)