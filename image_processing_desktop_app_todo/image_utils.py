import json
import os
import logging

# 创建日志记录器
def create_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s | 文件:%(filename)s,函数:%(funcName)s')
    return logging


# 加载语言数据
def load_language_data():
    print(os.getcwd())
    if os.path.exists('language.json') and os.path.getsize('language.json') > 0:
        with open('language.json', 'r') as f:
            try:
                language_data = json.load(f)
                return language_data
            except json.JSONDecodeError:
                print("JSONDecodeError: Could not parse the file")
    else:
        print("File does not exist or the file is empty")

# 写入语言数据
def write_language_data(language_data, key, value):
    language_data[key] = value
    with open('language.json', 'w', encoding='utf-8') as f:
        json.dump(language_data, f, ensure_ascii=False, indent=4)


#################### 以下是载入代码 ####################
language_data = load_language_data()
logging = create_logger()
    
    

