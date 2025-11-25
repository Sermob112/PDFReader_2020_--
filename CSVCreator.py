import pandas as pd
import glob


path = 'CSVforPurchases\*.csv'


all_files = glob.glob(path)

#
combined_csv = pd.DataFrame()

for filename in all_files:

    df = pd.read_csv(filename, skiprows=[0], encoding='cp1251', sep=';') 
   
    combined_csv = pd.concat([combined_csv, df], ignore_index=True)

combined_csv.to_csv('Все закупки 30-1.csv', index=False, encoding='utf-8')

print("Объединение завершено! Результат сохранен в 'Все закупки 30-1.csv'")