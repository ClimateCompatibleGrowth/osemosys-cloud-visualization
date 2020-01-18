import random
import wget
import os
from zipfile import ZipFile

def download_files(url):
    random_number = random.randint(1,99999)
    zip_file_name = f'tmp/csv_{random_number}.zip'
    folder_name = f'tmp/csv_{random_number}'
    wget.download(url, zip_file_name)
    zip_path = os.path.join(os.getcwd(), zip_file_name)
    with ZipFile(zip_path, 'r') as zipObj:
        zipObj.extractall(folder_name)
    return os.path.join(os.getcwd(), f'{folder_name}/csv/')

def vietnam_files():
    return os.path.join(os.getcwd(), 'data/vietnam/csv/')
