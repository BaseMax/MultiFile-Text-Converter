#
# Max Base
# https://github.com/BaseMax/MultiFile-Text-Converter
#

import os
import re
import random
import string
import pandas as pd

ARABIC_PERSIAN_PATTERN = r'[\u0600-\u06FF\u0750-\u077F\u0590-\u05FF]+'

def is_arabic_or_persian(text):
	return bool(re.search(ARABIC_PERSIAN_PATTERN, text))

def generate_random_id(existing_ids):
	while True:
		random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
		if random_id not in existing_ids:
			return random_id

def process_file(file_path, lines_map):
	existing_ids = {}
	with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
		lines = file.readlines()
		for i, line in enumerate(lines):
			if is_arabic_or_persian(line):
				match = re.match(r'^(\s*).*?(\s*)$', line)
				if match:
					leading_space = match.group(1)
					trailing_space = match.group(2)
					line_content = line.strip()
					if line_content not in existing_ids:
						random_id = generate_random_id(existing_ids)
						existing_ids[line_content] = random_id
					else:
						random_id = existing_ids[line_content]
					lines_map[random_id] = line_content
					lines[i] = f"{leading_space}<<<$$${random_id}$$$>>>{trailing_space}"

def process_files():
	lines_map = {}
	for root, dirs, files in os.walk("."):
		for file in files:
			if file.endswith(".config") or file.endswith(".aspx") or file.endswith(".ascx"):
				file_path = os.path.join(root, file)
				print(file_path)
				process_file(file_path, lines_map)

	df = pd.DataFrame(list(lines_map.items()), columns=['Random ID', 'Original Line'])

	excel_filename = "all_texts.xlsx"
	df.to_excel(excel_filename, index=False, engine='xlsxwriter')

	print(f"Generated {excel_filename} containing all text mappings.")

if __name__ == "__main__":
	process_files()
