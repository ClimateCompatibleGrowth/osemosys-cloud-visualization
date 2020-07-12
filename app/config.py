import random
import wget
import os
from zipfile import ZipFile


class Config:
    def __init__(self, input_string):
        self.input_string = input_string

    def csv_folder_path(self):
        return self.__input_path()

    def data_file_path(self):
        # self.input_string only works locally for now
        return os.path.join(os.getcwd(), 'data', self.input_string, 'data.txt')

    def __input_path(self):
        if self.input_string in ['bolivia', 'ethiopia', 'vietnam', 'indonesia']:
            return self.__local_csv_folder_for(self.input_string)
        else:
            return __download_files(self.input_string)

    def __local_csv_folder_for(self, model_name):
        return os.path.join(os.getcwd(), 'data', model_name, 'csv')

    def __download_files(self, input_string):
        random_number = random.randint(1, 99999)
        zip_file_name = f'csv_{random_number}.zip'
        folder_name = f'csv_{random_number}'

        zip_path = os.path.join(os.getcwd(), 'tmp', zip_file_name)
        wget.download(input_string, zip_path)
        folder_path = os.path.join(os.getcwd(), 'tmp', folder_name)

        with ZipFile(zip_path, 'r') as zipObj:
            zipObj.extractall(folder_path)

        return os.path.join(os.getcwd(), 'tmp', folder_name, 'csv')
