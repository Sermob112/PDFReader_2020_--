import fitz

# def pdf_to_txt_with_mupdf(pdf_path, txt_path):
#     doc = fitz.open(pdf_path)
#     with open(txt_path, 'w', encoding='utf-8') as txt_file:
#         for page in doc:
#           
#             blocks = page.get_text("dict")["blocks"]
#             for block in blocks:
#                 if "lines" in block:
#                     for line in block["lines"]:
#                         for span in line["spans"]:
#                             font = span["font"]
#                             size = span["size"]
#                             text = span["text"]
                            
#                             
#                             if ('Arial-Black' in font and 
#                                 abs(size - 22) < 1):  # размер около 22pt
#                                 txt_file.write(f"ЗАГОЛОВОК: {text}\n")
#                             else:
#                                 txt_file.write(text)
#                         txt_file.write("\n")

# # pip install PyMuPDF
# pdf_file_path = "SS 1998.pdf"
# txt_file_path = 'output2.txt'

# pdf_to_txt_with_mupdf(pdf_file_path, txt_file_path)


import fitz  
import os

# Указываем пути
input_folder = "2. Файлы для БД"  
output_folder = "Raw_text"  


os.makedirs(output_folder, exist_ok=True)


for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"):  
        pdf_path = os.path.join(input_folder, filename)
        
        
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_path = os.path.join(output_folder, txt_filename)
        
      
        doc = fitz.open(pdf_path)
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            for page in doc:
                text = page.get_text()
                txt_file.write(text + "\n")
        
        print(f"Сохранено: {txt_path}")
