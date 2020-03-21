import random
import wget
import os
from zipfile import ZipFile


class Config:
    def __init__(self, url):
        self.url = url

    def csv_folder_path(self):
        return self.__input_path()

    def data_file_path(self):
        # self.url only works locally for now
        return os.path.join(os.getcwd(), 'data', self.url, 'data.txt')

    def __input_path(self):
        if self.url in ['bolivia', 'ethiopia', 'vietnam', 'indonesia']:
            return self.__local_csv_folder_for(self.url)
        else:
            return __download_files(self.url)

    def __local_csv_folder_for(self, model_name):
        return os.path.join(os.getcwd(), 'data', model_name, 'csv')

    def __download_files(self, url):
        random_number = random.randint(1, 99999)
        zip_file_name = f'csv_{random_number}.zip'
        folder_name = f'csv_{random_number}'

        zip_path = os.path.join(os.getcwd(), 'tmp', zip_file_name)
        wget.download(url, zip_path)
        folder_path = os.path.join(os.getcwd(), 'tmp', folder_name)

        with ZipFile(zip_path, 'r') as zipObj:
            zipObj.extractall(folder_path)

        return os.path.join(os.getcwd(), 'tmp', folder_name, 'csv')
