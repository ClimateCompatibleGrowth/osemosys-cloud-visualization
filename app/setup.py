import random
import wget
import os
from zipfile import ZipFile

def input_path(url):
    if url == 'bolivia':
        return bolivia_files()
    elif url == 'ethiopia':
        return ethiopia_files()
    elif url == 'vietnam':
        return vietnam_files()
    else:
        return download_files(url)

def ethiopia_files():
    return os.path.join(os.getcwd(), 'data', 'ethiopia', 'csv')

def bolivia_files():
    return os.path.join(os.getcwd(), 'data', 'bolivia', 'csv')

def vietnam_files():
    return os.path.join(os.getcwd(), 'data', 'vietnam', 'csv')

def download_files(url):
    random_number = random.randint(1,99999)
    zip_file_name = f'csv_{random_number}.zip'
    folder_name = f'csv_{random_number}'

    zip_path = os.path.join(os.getcwd(), 'tmp', zip_file_name)
    wget.download(url, zip_path)
    folder_path = os.path.join(os.getcwd(), 'tmp', folder_name)

    with ZipFile(zip_path, 'r') as zipObj:
        zipObj.extractall(folder_path)

    return os.path.join(os.getcwd(), 'tmp', folder_name, 'csv')
