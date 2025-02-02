import pandas as pd
from openpyxl import Workbook
import re

def table_merger_raw():
    file_path = 'HHI_PerformanceRecord_2024-tabl.xlsx'

    # Чтение всех листов из файла
    xls = pd.ExcelFile(file_path)

    # Словарь для хранения данных по названиям
    data_dict = {}

    # Проход по всем листам
    for sheet_name in xls.sheet_names:
        # Чтение данных из листа, пропуская первую строку
        df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str, header=1)
        df = df.drop([0, 4])
        # Получение названия из первой строки исходного файла
        title = pd.read_excel(xls, sheet_name=sheet_name, nrows=0).columns[0]
        
        # Очистка названия от недопустимых символов
        cleaned_title = re.sub(r'[\\/*?:[\]]', '', title)
        
        # Разделение названия на "Компания" и "Тип судна"
        if ':' in title:
            company, ship_type = title.split(':', 1)  # Разделяем по первому двоеточию
            company = company.strip()  # Убираем лишние пробелы
            ship_type = ship_type.strip()
        else:
            company = title  # Если двоеточия нет, используем всё название как "Компания"
            ship_type = ''   # "Тип судна" будет пустым
        
        # Добавление новых столбцов
        df['Компания'] = company
        df['Тип судна'] = ship_type
        
        # Перестановка столбцов: "Компания" и "Тип судна" становятся первыми
        cols = ['Компания', 'Тип судна'] + [col for col in df.columns if col not in ['Компания', 'Тип судна']]
        df = df[cols]
        
        # Обработка столбцов MAIN ENGINE и OWNER
        for column in ['MAIN ENGINE', 'OWNER']:
            if column in df.columns:
                # Заполнение пропущенных значений
                df[column] = df[column].fillna('')
                
                # Объединение строк в столбце
                df[column] = df.groupby(df.index)[column].transform(lambda x: ' '.join(x))
                
                # Удаление дубликатов, если они возникли после объединения
                df = df.drop_duplicates(subset=df.columns.difference([column]))

        
        
        # Добавление данных в словарь
        if cleaned_title not in data_dict:
            data_dict[cleaned_title] = []
        data_dict[cleaned_title].append(df)

    # Создание нового Excel файла
    new_wb = Workbook()
    new_wb.remove(new_wb.active)  # Удаление дефолтного листа

    # Запись данных в новый файл
    for title, dfs in data_dict.items():
        # Создание нового листа для каждого уникального названия
        ws = new_wb.create_sheet(title=title[:31])  # Ограничение длины названия до 31 символа
        
        # Объединение всех таблиц с одинаковым названием
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Запись заголовков столбцов в первую строку
        ws.append(combined_df.columns.tolist())
        
        # Запись данных в лист
        for r in pd.DataFrame(combined_df).itertuples(index=False, name=None):
            ws.append(r)

    # Сохранение нового файла
    new_wb.save('Tables\combined_data_with_columns_3.xlsx')

# Вызов функции
# table_merger_raw()




def table_merger_combine():
    file_path = 'Tables\\combined_data_with_columns_3.xlsx'  # Укажите путь к вашему файлу
    xl = pd.ExcelFile(file_path)

    # Создаем словарь для хранения данных по компаниям
    company_data = {}

    # Проходим по всем страницам Excel-файла
    for sheet_name in xl.sheet_names:
        # Читаем данные с текущей страницы
        df = xl.parse(sheet_name)
        
        # Определяем название компании (первый столбец)
        company_column = df.columns[0]
        
        # Группируем данные по компаниям
        for company_name, group in df.groupby(company_column):
            if company_name not in company_data:
                company_data[company_name] = []
            company_data[company_name].append(group)

    # Объединяем данные для каждой компании в одну таблицу
    for company_name, data_frames in company_data.items():
        combined_df = pd.concat(data_frames, ignore_index=True)
        
        # Сохраняем объединенную таблицу в новый Excel-файл
        output_file = f'Tables\{company_name}.xlsx'
        combined_df.to_excel(output_file, index=False)
        
        print(f'Данные для компании {company_name} сохранены в файл {output_file}')


# table_merger_combine()


def table_merger_combine_2():
    file_path = 'Tables\\combined_data_with_columns_3.xlsx'  # Укажите путь к вашему файлу
    xl = pd.ExcelFile(file_path)

    # Создаем словарь для хранения данных по компаниям
    company_data = {}

    # Проходим по всем страницам Excel-файла
    for sheet_name in xl.sheet_names:
        # Читаем данные с текущей страницы
        df = xl.parse(sheet_name)
        
        # Определяем название компании (первый столбец)
        company_column = df.columns[0]
        
        # Группируем данные по компаниям
        for company_name, group in df.groupby(company_column):
            if company_name not in company_data:
                company_data[company_name] = []
            company_data[company_name].append(group)

    # Создаем ExcelWriter для записи в один файл
    output_file = 'Tables\\combined_companies.xlsx'
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        # Объединяем данные для каждой компании в одну таблицу и записываем на отдельный лист
        for company_name, data_frames in company_data.items():
            combined_df = pd.concat(data_frames, ignore_index=True)
            
            # Записываем объединенную таблицу на отдельный лист
            combined_df.to_excel(writer, sheet_name=company_name, index=False)
            
            print(f'Данные для компании {company_name} сохранены на лист {company_name} в файле {output_file}')

# table_merger_combine_2()
        
def table_merger_second_try():
    file_path = 'Tables\\combined_data_with_columns_2.xlsx'  # Укажите путь к вашему файлу
   
    xl = pd.ExcelFile(file_path)

    # Создаем пустой DataFrame для хранения объединенных данных
    merged_df = pd.DataFrame()

    # Проходим по каждому листу в файле
    for sheet_name in xl.sheet_names:
        # Читаем данные из листа
        df = xl.parse(sheet_name)
        
        # Если merged_df пустой, просто копируем в него данные из первого листа
        if merged_df.empty:
            merged_df = df
        else:
            # Объединяем данные по столбцу "Компания"
            merged_df = pd.merge(merged_df, df, on='Компания', how='outer')

    output_file = 'Tables\\merged_tables.xlsx'
    merged_df.to_excel(output_file, index=False)

# table_merger_second_try()
    

def normalize_columns(file_path):
    # Создаем пустой список для хранения названий столбцов
    all_columns = []

    # Читаем Excel-файл
    xls = pd.ExcelFile(file_path)

    # Создаем словарь для хранения данных каждого листа
    sheet_data = {}

    # Проходим по всем листам в файле
    for sheet_name in xls.sheet_names:
        # Читаем данные с текущего листа
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Нормализуем названия колонок
        df.columns = [normalize_column_name(col) for col in df.columns]
        
        # Сохраняем измененный DataFrame в словарь
        sheet_data[sheet_name] = df

    # Сохраняем все листы обратно в файл
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for sheet_name, df in sheet_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

def normalize_column_name(column):
    normalization_rules = {
        'DIMENSIONS': 'DIMENSIONS (LBP×B×D×d)',
        'DIMENSIONS (LOA×B×D×d)': 'DIMENSIONS (LBP×B×D×d)',
        'DIMENSIONS (LOA×B×D×t(d))': 'DIMENSIONS (LBP×B×D×d)',
        'TYPE OF VESSEL': 'Type of Vessel',
        'Type of Vessel.1': 'Type of Vessel',
        'MAIN ENGINE': 'Main Engine',
        'cbm (m3)': 'CBM(m3)',
        'capACITY': 'capacity',
        'capacity.1': 'capacity',
        'OWNER': 'Owner',
        'COUNTRY': 'Country',
        'countrY': 'Country',
        'CLASS': 'Class',
        'HULL NO.': 'HULL',
        'ship name': 'Ship Name',
        'DWT': 'dwt',
        'MAIN': 'Main Engine',
        'Тип судна': 'Type of Vessel',
        'Компания': 'Owner',
        'Delivery Date': 'Delivery'
    }

    # Приводим к нижнему регистру для унификации
    lower_column = column.lower()

    # Ищем соответствие в словаре
    for key, value in normalization_rules.items():
        if key.lower() == lower_column:
            return value

    # Если соответствие не найдено, оставляем исходное значение
    return column

# Укажите путь к вашему файлу
file_path = 'Tables\\combined_data_with_columns_3.xlsx'

# Вызов функции для нормализации колонок
# normalize_columns(file_path)


def cleaner():
    file_path = 'Tables\\HII по названию.xlsx'  # Укажите путь к вашему файлу
    df = pd.read_excel(file_path)

    # Функция для объединения текста в одной ячейке
    def join_text(cell):
        if isinstance(cell, str):
            return ' '.join(line.strip() for line in cell.splitlines())
        return cell

    # Примените функцию к колонке 'Owner'
    df['Owner'] = df['Owner'].apply(join_text)

    # Сохраните изменения обратно в файл Excel
    df.to_excel('Tables\\updated_file.xlsx', index=False)
cleaner()