import random
import wget
import os
from zipfile import ZipFile
from app.generate_csv_files import generate_csv_files
import functools


class Config:
    def __init__(self, input_string):
        self.input_string = input_string

    def csv_folder_path(self):
        csv_path = os.path.join(self.__base_folder_path(), 'csv')
        if not os.path.exists(csv_path):
            self.__generate_csv()

        return csv_path

    def data_file_path(self):
        return os.path.join(self.__base_folder_path(), 'data.txt')

    def __results_file_path(self):
        return os.path.join(self.__base_folder_path(), 'result.txt')

    def __base_folder_path(self):
        if self.input_string in ['bolivia', 'ethiopia', 'vietnam', 'indonesia', 'mexico']:
            return os.path.join(os.getcwd(), 'data', self.input_string)
        elif self.input_string.startswith('http'):
            return self.__download_files(self.input_string)
        elif 'uploaded' in self.input_string:
            return self.input_string
        else:
            raise NameError('NoFolderFound')

    @functools.lru_cache(maxsize=128)
    def __download_files(self, input_string):
        random_number = random.randint(1, 99999)
        zip_file_name = f'osemosys_result_{random_number}.zip'
        folder_name = f'osemosys_result_{random_number}'

        zip_path = os.path.join(os.getcwd(), 'tmp', zip_file_name)
        wget.download(input_string, zip_path)
        folder_path = os.path.join(os.getcwd(), 'tmp', folder_name)

        with ZipFile(zip_path, 'r') as zipObj:
            zipObj.extractall(folder_path)

        return os.path.join(os.getcwd(), 'tmp', folder_name)

    def __generate_csv(self):
        generate_csv_files(
            self.data_file_path(),
            self.__results_file_path(),
            self.__base_folder_path()
        )
