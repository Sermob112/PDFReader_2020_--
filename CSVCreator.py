import pandas as pd
import glob

# Путь к папке с CSV-файлами (замените на ваш путь)
path = 'CSVforPurchases\*.csv'

# Список всех CSV-файлов в папке
all_files = glob.glob(path)

# Создаем пустой DataFrame для хранения объединенных данных
combined_csv = pd.DataFrame()

# Читаем и объединяем файлы
for filename in all_files:
    # Читаем файл, пропуская первую строку (если заголовок во второй строке)
    df = pd.read_csv(filename, skiprows=[0], encoding='cp1251', sep=';') 
    
    # Добавляем данные в общий DataFrame
    combined_csv = pd.concat([combined_csv, df], ignore_index=True)

# Сохраняем объединенный файл
combined_csv.to_csv('Все закупки 30-1.csv', index=False, encoding='utf-8')

print("Объединение завершено! Результат сохранен в 'Все закупки 30-1.csv'")