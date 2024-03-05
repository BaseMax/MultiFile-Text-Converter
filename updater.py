#
# Max Base
# https://github.com/BaseMax/MultiFile-Text-Converter
#

import os
import re
import pandas as pd

def update_files(excel_file):
    df = pd.read_excel(excel_file)
    id_to_text_mapping = dict(zip(df['Random ID'], df['Translated Line']))

    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".config") or file.endswith(".aspx") or file.endswith(".ascx"):
                file_path = os.path.join(root, file)
                print(file_path)
                update_file(file_path, id_to_text_mapping)

def update_file(file_path, id_to_text_mapping):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        modified_lines = []

        for line in lines:
            match = re.search(r'<<<\$\$\$(.*?)\$\$\$>>>', line)
            if match:
                random_id = match.group(1)
                if random_id in id_to_text_mapping:
                    translated_text = id_to_text_mapping[random_id]
                    modified_lines.append(translated_text + '\n')
                else:
                    modified_lines.append(line)
            else:
                modified_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)

if __name__ == "__main__":
    excel_filename = "translated_texts.xlsx"
    update_files(excel_filename)
    print("Files updated with new translated text.")
