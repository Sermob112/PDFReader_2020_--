import fitz  # PyMuPDF

def extract_tanker_data(pdf_path):
    with fitz.open(pdf_path) as doc:
        found_tanker = False
        found_technical = False
        extracted_text = []
        
        for page in doc:
            text = page.get_text("text")
            lines = text.split("\n")

            for line in lines:
                if "AL ADAILIAH – Oil tanker" in line:
                    found_tanker = True
                    extracted_text.append(line)

                if "TECHNICAL PARTICULARS" in line:
                    found_technical = True
                
                if found_technical:
                    extracted_text.append(line)
        
        return "\n".join(extracted_text)

pdf_path = "Test.pdf"  # Укажите путь к файлу
# result = extract_tanker_data(pdf_path)

import fitz  # PyMuPDF

import fitz  # PyMuPDF

def extract_ships_and_descriptions(pdf_path):
    ships_data = {}
    current_ship = None

    with fitz.open(pdf_path) as doc:
        for page in doc:
            text_info = page.get_text("dict")  # Получаем структуру текста
            for block in text_info["blocks"]:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span["text"].strip()
                        font_size = span["size"]
                        font_name = span["font"]

                        
                        if font_size == 22 and "Arial-Black" in font_name:
                            current_ship = text  # Запоминаем название судна
                            ships_data[current_ship] = {}  # Создаем пустой словарь для характеристик

                    
                        elif current_ship and font_size == 7.5 and ("Helvetica" in font_name or "Helvetica-Bold" in font_name):
                            parts = text.split("...")  # Разделяем характеристику и значение
                            if len(parts) > 1:
                                key = parts[0].strip().rstrip(":")  # Убираем пробелы и двоеточие
                                value = parts[-1].strip()
                                ships_data[current_ship][key] = value
    
    return ships_data

pdf_path = "Test.pdf"  # Укажите путь к вашему файлу
ships_info = extract_ships_and_descriptions(pdf_path)

# Выводим результат
for ship, attributes in ships_info.items():
    print(f"Судно: {ship}")
    for key, value in attributes.items():
        print(f"{key}: {value}")
    print("-" * 50)
