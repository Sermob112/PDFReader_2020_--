import fitz
import re
import pandas as pd

def pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    header_font_size = 22
    headers = []
    top_margin = 50
    bottom_margin = 50

    for page in doc:
        page_height = page.rect.height
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            is_page_number = False
            if b["type"] == 0:
                if b["bbox"][3] < top_margin or b["bbox"][3] > page_height - bottom_margin:
                    if re.fullmatch(r"\d+", b["lines"][0]["spans"][0]["text"].strip()):
                        is_page_number = True

            for l in b["lines"]:
                for s in l["spans"]:
                    if s["size"] >= header_font_size and "bold":
                        headers.append(s["text"])  # Сохраняем заголовки
                    elif not is_page_number:
                        text += s["text"]
                if not is_page_number:
                    text += "\n"
            if not is_page_number:
                text += "\n"

    text = re.sub(r"\.{2,}", "", text)

    # Удаляем "Significant Ships of 2020"
    text = text.replace("Significant Ships of 2020", "")

    # Удаляем лишний текст между "Total number of sister ships still on order" и "TECHNICAL PARTICULARS"
    text = re.sub(r"(Total number of sister ships still on order:\s*)(.*?)(\n.*?)(TECHNICAL PARTICULARS)", r"\1\2\n\4", text, flags=re.DOTALL | re.IGNORECASE)

    # Исправляем разорванные единицы измерения (m\n3) → (m³)
    text = re.sub(r"\(m\s*\n\s*3\)", "(m³)", text)
    with open("text.txt", "w", encoding="utf-8") as file:
        file.write(text)
    return text, headers

def parse_text_to_dataframe(text, headers):
    lines = text.split("\n")
    data = []

    current_key = None
    current_value = ""


    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Если строка содержит "ключ: значение"
        if ":" in line:
            if current_key:
                data.append([current_key, current_value.strip()])
            parts = line.split(":", 1)
            current_key = parts[0].strip()
            current_value = parts[1].strip()
        else:
            current_value += " " + line.strip()

        # Вставляем **заголовок судна на всю строку перед "Shipbuilder"**
        if current_key == "Shipbuilder":
            data.append(["", ""])  # Пустая строка перед заголовком
            data.append(["", ""])  # Пустая строка перед заголовком
            data.append(["", ""])  # Пустая строка перед заголовком



    if current_key:
        data.append([current_key, current_value.strip()])

    return pd.DataFrame(data, columns=["Параметр", "Значение"])

def save_to_excel(df, excel_path):
    df.to_excel(excel_path, index=False, engine="openpyxl")

if __name__ == "__main__":
    pdf_file_path = "Test.pdf"
    excel_file_path = "output.xlsx"

    text, headers = pdf_to_text(pdf_file_path)
    df = parse_text_to_dataframe(text, headers)
    save_to_excel(df, excel_file_path)

    print(f"Файл успешно сохранен: {excel_file_path}")
