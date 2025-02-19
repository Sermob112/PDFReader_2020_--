with open("2003.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

formatted_lines = []
i = 0

# Символы, после которых нужно объединять строки
continuation_symbols = ("/", "&", "-", "=", "+", "~","(",".")

while i < len(lines):
    line = lines[i].strip()  # Убираем лишние пробелы

    # Проверяем, начинается ли следующая строка с цифры
    def next_line_starts_with_digit(idx):
        return idx < len(lines) and lines[idx].strip() and lines[idx].strip()[0].isdigit()

    # Объединяем строки для "Classification society and notations:"
    if line.startswith("Classification society and notations:"):
        merged_line = line
        i += 1
        while i < len(lines) and not lines[i].strip().startswith("Propulsion"):
            merged_line += " " + lines[i].strip()
            i += 1
        formatted_lines.append(merged_line)

    # Объединяем строки для "Engine make/type:"
    elif line.startswith("Engine make/type:"):
        merged_line = line
        i += 1
        while i < len(lines) and not (lines[i].strip().startswith("Type of fuel:") or lines[i].strip().startswith("Alternator make/type:") or lines[i].strip().startswith("Output/speed of each set:")):
            merged_line += " " + lines[i].strip()
            i += 1
        formatted_lines.append(merged_line)

    # Объединяем строки для "Alternator make/type:"
    elif line.startswith("Alternator make/type:"):
        merged_line = line
        i += 1
        while i < len(lines) and not (lines[i].strip().startswith("Output/speed of each set:") or lines[i].strip().startswith("Output/speed of each set:") 
                                      or lines[i].strip().startswith("Manufacturer:") or lines[i].strip().startswith("Number:")):
            merged_line += " " + lines[i].strip()
            i += 1
        formatted_lines.append(merged_line)

    elif line.startswith("Alternator make/type:"):
        merged_line = line
        i += 1
        while i < len(lines) and not (lines[i].strip().startswith("Output/speed of each set:") or lines[i].strip().startswith("Output/speed of each set:") 
                                      or lines[i].strip().startswith("Manufacturer:") or lines[i].strip().startswith("Number:")):
            merged_line += " " + lines[i].strip()
            i += 1
        formatted_lines.append(merged_line)

    elif line.startswith("Number of each:"):
        merged_line = line
        i += 1
        while i < len(lines) and not (lines[i].strip().startswith("Make:") or lines[i].strip().startswith("Type:") 
                                      or lines[i].strip().startswith("Crew:") or lines[i].strip().startswith(" Designer:")):
            merged_line += " " + lines[i].strip()
            i += 1
        formatted_lines.append(merged_line)

    elif line.startswith("Tasks:"):
        merged_line = line
        i += 1
        while i < len(lines) and not (lines[i].strip().startswith("Performance:") or lines[i].strip().startswith("Number:")):
            merged_line += " " + lines[i].strip()
            i += 1
        formatted_lines.append(merged_line)

    elif line.startswith("Energy Saving Technologies:"):
        merged_line = line
        i += 1
        while i < len(lines) and not (lines[i].strip().startswith("Hull coatings:") or lines[i].strip().startswith("Contract date:") 
                                      or lines[i].strip().startswith("Delivery date:")):
            merged_line += " " + lines[i].strip()
            i += 1
        formatted_lines.append(merged_line)

    # Обрабатываем строки с "Is" и "Integrated"
    elif line.startswith("Is") or line.startswith("Integrated") or line.startswith("Ltd.") or line.startswith("Inc.") or line.startswith("&") or line.startswith("("):
        if formatted_lines and not formatted_lines[-1].endswith('?'):  # Чтобы избежать ошибки при комбинировании вопросов
            formatted_lines[-1] += " " + line
        else:
            formatted_lines.append(line)
        i += 1

    # Обрабатываем строки с символами "/", "&", "-", "=", "+"
    elif any(line.endswith(symbol) for symbol in continuation_symbols) or next_line_starts_with_digit(i + 1):
        merged_line = line
        i += 1
        while i < len(lines) and (any(lines[i].strip().endswith(symbol) for symbol in continuation_symbols) or next_line_starts_with_digit(i)):
            merged_line += " " + lines[i].strip()
            i += 1
        if i < len(lines) and not lines[i].strip().startswith(("Classification society and notations:", "Engine make/type:", "Manufacturer:","Type:")):
            merged_line += " " + lines[i].strip()
            i += 1
        
        # Разделяем "Mooring equipment", если оно случайно слилось
        if "Mooring equipment" in merged_line:
            merged_line, mooring_part = merged_line.split("Mooring equipment", 1)
            formatted_lines.append(merged_line.strip())
            formatted_lines.append("Mooring equipment" + mooring_part.strip())
        else:
            formatted_lines.append(merged_line)

    else:
        formatted_lines.append(line)
        i += 1

# Запись обратно в файл
with open("formatted_text_2003.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(formatted_lines))
