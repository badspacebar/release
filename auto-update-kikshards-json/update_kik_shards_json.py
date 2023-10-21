import os
import json
import hashlib
import time

def get_file_info(file_path):
    filename = os.path.basename(file_path)
    english_name = filename.rsplit('.', 1)[0]
    chinese_name = english_name  # Assuming the Chinese name is the same as the English name
    md5_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    last_upload_time = time.ctime(os.path.getmtime(file_path))
    return {
        'filename': filename,
        'md5': md5_hash,
        'last_upload_time': last_upload_time,
        'chinese_name': chinese_name,
        'english_name': english_name,
        'chinese_description': 'To be added',
        'english_description': 'To be added'
    }

def main():
    file_info_list = []
    for root, dirs, files in os.walk('files/kik-shards'):
        for file in files:
            file_path = os.path.join(root, file)
            file_info = get_file_info(file_path)
            file_info_list.append(file_info)
    
    with open('kik-shards.json', 'w', encoding='utf-8') as f:
        json.dump(file_info_list, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
