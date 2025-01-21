import fitz
import re

def pdf_to_text_with_page_number_removal(pdf_path, txt_path):
    doc = fitz.open(pdf_path)
    text = ""
    header_font_size = 22
    page_height = 0 # будем определять высоту страницы

    # Пределы для определения номеров страниц (экспериментальные значения, нужно подбирать)
    top_margin = 50  # 50 пикселей от верха страницы
    bottom_margin = 50 # 50 пикселей от низа

    for page in doc:
        page_height = page.rect.height # получаем высоту страницы
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            # Проверяем, попадает ли блок в область номера страницы
            is_page_number = False
            if b["type"] == 0:  # 0 - текстовый блок
                # Если блок в пределах отступа от верхнего или нижнего края, считаем что это номер
                if b["bbox"][3] < top_margin or b["bbox"][3] > page_height - bottom_margin:
                    # И если в блоке только цифры
                    if re.fullmatch(r"\d+", b["lines"][0]["spans"][0]["text"].strip()):
                        is_page_number = True

            for l in b["lines"]:
                for s in l["spans"]:
                    if s["size"] >= header_font_size and "bold" in s["font"].lower():
                        text += f"<h1>{s['text']}</h1>\n"
                    elif not is_page_number:
                        text += s["text"]
                if not is_page_number:
                    text += "\n"
            if not is_page_number:
                text += "\n"

    # Удаляем многоточия с помощью регулярного выражения
    text = re.sub(r"\.{2,}", "", text)

    # Удаляем фразу "Significant Ships of 2020"
    text = text.replace("Significant Ships of 2020", "")

    # Удаляем текст между "Total number of sister ships still on order: <значение>" и "TECHNICAL PARTICULARS"
    text = re.sub(r"(Total number of sister ships still on order:\s*)(.*?)(\n.*?)(TECHNICAL PARTICULARS)", r"\1\2\n\4", text, flags=re.DOTALL | re.IGNORECASE)

    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

if __name__ == "__main__":
    pdf_file_path = 'Test.pdf'
    txt_file_path = 'output.txt'
    pdf_to_text_with_page_number_removal(pdf_file_path, txt_file_path)
    print(f"Текст успешно сохранен в {txt_file_path}")