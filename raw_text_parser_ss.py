import re
import os

import re
import os

import re

import re

def clean_text_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()  # Читаем файл построчно

    cleaned_lines = []
    inside_deletion = False  # Флаг удаления строк
    merged_line = ""  # Переменная для слияния строк

    # Список строк, с которых начинается удаление
    start_patterns = [
        r"Delivery date",
        r"IMO number",
        r"па"  # Добавляйте сюда другие условия
    ]
    end_pattern = r"TECHNICAL PARTICULARS"  # Конец удаления

    for i, line in enumerate(lines):
        # Удаление многоточия и добавление двоеточия если его нет

        
        line = re.sub(r':\s*\.{3,}', ':', line)  # Первый вариант (с двоеточием)
        # line = re.sub(r'(\w+)\s*\.{3,}\s*(\d+)', r'\1: \2', line)  # Второй вариант (без двоеточия)
        # line = re.sub(r'(\w+\s*\w*)\s*\.{3,}\s*(\w+)', r'\1: \2', line)

        line = re.sub(r'\s*\.+\s*', ' : ', line) 
        # Проверка на продолжение предыдущей строки
        if re.match(r'^[\d\$%№\\&\t\s]+', line.strip()):
            # Если текущая строка начинается с цифры или спец.символа
            if merged_line:
                # Добавляем к предыдущей строке без переноса строки
                merged_line += line.strip()
                cleaned_lines[-1] = merged_line + '\n'
                merged_line = ""
            continue
        if "SIGNIFICANT SMALL SHIPS" in line or "Significant ShipS" in line:
            continue
        if merged_line:
            # Если была предыдущая незавершенная строка
            cleaned_lines[-1] = merged_line + line
            merged_line = ""
        else:
            # Обычная обработка строк
            if any(re.match(pattern, line) for pattern in start_patterns):  
                inside_deletion = True  # Начинаем удалять строки
                cleaned_lines.append(line)  # Оставляем эту строку
            
            elif re.match(end_pattern, line):
                inside_deletion = False  # Конец удаления
                cleaned_lines.append(line)  # Оставляем эту строку
            
            elif not inside_deletion:
                # Проверка на возможный перенос следующей строки
                if i + 1 < len(lines) and re.match(r'^[\d\$%№\\]', lines[i+1].strip()):
                    merged_line = line.rstrip()
                else:
                    cleaned_lines.append(line)

    with open(output_path, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)  # Записываем очищенные строки

    print(f"Файл обработан: {output_path}")



# Пример обработки всех файлов в папке
    
# input = "Raw_text sss\SSS 2001.txt"
# output= "Processed_text_ss\Proccesed_SS 2001.txt"
# clean_text_file(input,output)
    
input_folder = "raw_text sss"
output_folder = "Processed_text_ss_test"
os.makedirs(output_folder, exist_ok=True)  # Создаем папку, если её нет

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):  # Обрабатываем только TXT-файлы
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        clean_text_file(input_path, output_path)
