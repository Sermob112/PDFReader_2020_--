import fitz
import re

import os

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
            if "lines" not in b:  # Пропускаем блоки без текста (например, изображения)
                continue

            is_page_number = False
            if b["type"] == 0:
                if b["bbox"][3] < top_margin or b["bbox"][3] > page_height - bottom_margin:
                    first_span = b["lines"][0]["spans"][0] if b["lines"] and b["lines"][0]["spans"] else None
                    if first_span and re.fullmatch(r"\d+", first_span["text"].strip()):
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

    text = text.replace("Significant Ships of 1998", "")


    text = re.sub(r"(Total number of sister ships still on order:\s*)(.*?)(\n.*?)(TECHNICAL PARTICULARS)", r"\1\2\n\4", text, flags=re.DOTALL | re.IGNORECASE)

    text = re.sub(r"\(m\s*\n\s*3\)", "(m³)", text)

    with open("Raw_text\\sss 2018.txt", "w", encoding="utf-8") as file:
        file.writelines(text)
    
    return text, headers

pdf_to_text("2. Файлы для БД\\SSS 2018.pdf")