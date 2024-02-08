import json
from googletrans import Translator

def translate_chunk(chunk):
    translator = Translator()
    translated_chunk = {}

    for key, value in chunk.items():
        if isinstance(value, dict):
            translated_chunk[key] = translate_chunk(value)
        else:
            translated_chunk[key] = translator.translate(value, src='en', dest='ru').text

    return translated_chunk

def read_json_chunk(file_path, start_line, end_line):
    chunk = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, start=1):
            if start_line <= i <= end_line:
                chunk.update(json.loads(line))
            elif i > end_line:
                break
    return chunk

# Define the file path and chunk size
file_path = 'locale-ru_RU.json'
lines_per_chunk = 500

# Calculate total number of lines in the file
total_lines = sum(1 for line in open(file_path, 'r', encoding='utf-8'))

# Process the file in chunks and save each chunk as a separate file
for start_line in range(1, total_lines + 1, lines_per_chunk):
    end_line = min(start_line + lines_per_chunk - 1, total_lines)
    chunk = read_json_chunk(file_path, start_line, end_line)
    translated_chunk = translate_chunk(chunk)
    
    # Determine the part number
    part_number = start_line // lines_per_chunk + 1

    # Save translated chunk to file
    output_file = f'part{part_number}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translated_chunk, f, ensure_ascii=False, indent=4)
