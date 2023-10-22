import os
import configparser
import hashlib

def get_file_info(file_path, existing_descriptions=None):
    if existing_descriptions is None:
        existing_descriptions = {}

    filename = os.path.basename(file_path)
    english_name = filename.rsplit('.', 1)[0]
    chinese_name = english_name  # Assuming the Chinese name is the same as the English name
    md5_hash = calculate_md5(file_path)  # Calculate MD5 hash

    # Use the existing descriptions if available, else use appropriate defaults
    chinese_description = existing_descriptions.get(filename, {}).get('chinese_description', '等待添加')
    english_description = existing_descriptions.get(filename, {}).get('english_description', 'To be added')
    level = existing_descriptions.get(filename, {}).get('level', 'low')  # Add level with default as 'low'

    return {
        'filename': filename,
        'md5': md5_hash,
        'chinese_name': chinese_name,
        'english_name': english_name,
        'chinese_description': chinese_description,
        'english_description': english_description,
        'level': level  # Include level in the returned info
    }

def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        md5 = hashlib.md5()
        while True:
            data = file.read(8192)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

def get_existing_descriptions(ini_path='kik-shards.ini'):
    if not os.path.exists(ini_path):
        return {}

    config = configparser.ConfigParser()
    config.read(ini_path)

    descriptions = {}
    for section in config.sections():
        filename = config[section].get('filename')
        if filename:
            descriptions[filename] = {
                'chinese_description': config[section].get('chinese_description', '等待添加'),
                'english_description': config[section].get('english_description', 'To be added'),
                'level': config[section].get('level', 'low')  # Read level from the INI file
            }
    return descriptions

def create_ini_config(file_info_list):
    # Sort the file_info_list alphabetically, but keep filenames starting with "KiK" at the front.
    sorted_file_info = sorted(file_info_list, key=lambda x: (not x['filename'].startswith('KiK'), x['filename']))
    
    config = configparser.ConfigParser()
    
    for idx, file_info in enumerate(sorted_file_info, start=1):
        section_name = f'File{idx}'
        config[section_name] = {
            'filename': file_info['filename'],
            'md5': file_info['md5'],
            'chinese_name': file_info['chinese_name'],
            'english_name': file_info['english_name'],
            'chinese_description': file_info['chinese_description'],
            'english_description': file_info['english_description'],
            'level': file_info['level']  # Write level to the INI file
        }
    
    return config

def main():
    existing_descriptions = get_existing_descriptions()

    file_info_list = []
    for root, dirs, files in os.walk('files/kik-shards'):
        for file in files:
            file_path = os.path.join(root, file)
            file_info = get_file_info(file_path, existing_descriptions)
            file_info_list.append(file_info)
    
    config = create_ini_config(file_info_list)
    
    with open('kik-shards.ini', 'w', encoding='utf-8') as f:
        config.write(f)

if __name__ == "__main__":
    main()
