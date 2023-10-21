import os
import configparser
import hashlib

def get_file_info(file_path):
    filename = os.path.basename(file_path)
    english_name = filename.rsplit('.', 1)[0]
    chinese_name = english_name  # Assuming the Chinese name is the same as the English name
    md5_hash = calculate_md5(file_path)  # Calculate MD5 hash
    return {
        'filename': filename,
        'md5': md5_hash,
        'chinese_name': chinese_name,
        'english_name': english_name,
        'chinese_description': 'To be added',
        'english_description': 'To be added'
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

def create_ini_config(file_info_list):
    config = configparser.ConfigParser()
    
    for idx, file_info in enumerate(file_info_list, start=1):
        section_name = f'File{idx}'
        config[section_name] = {
            'filename': file_info['filename'],
            'md5': file_info['md5'],
            'chinese_name': file_info['chinese_name'],
            'english_name': file_info['english_name'],
            'chinese_description': file_info['chinese_description'],
            'english_description': file_info['english_description']
        }
    
    return config

def main():
    file_info_list = []
    for root, dirs, files in os.walk('files/kik-shards'):
        for file in files:
            file_path = os.path.join(root, file)
            file_info = get_file_info(file_path)
            file_info_list.append(file_info)
    
    config = create_ini_config(file_info_list)
    
    with open('kik-shards.ini', 'w', encoding='utf-8') as f:
        config.write(f)

if __name__ == "__main__":
    main()
