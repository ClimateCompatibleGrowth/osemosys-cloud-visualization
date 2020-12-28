import random
import os


def process_uploaded_file(raw_contents):
    random_number = random.randint(1, 99999)
    uploaded_folder_path = os.path.join(os.getcwd(), 'tmp', 'uploaded', str(random_number))
    try:
        os.makedirs(uploaded_folder_path)
    except FileExistsError:
        pass
    content_type, content_string = raw_contents.split(',')

    write_and_extract_zip_file(content_string, uploaded_folder_path)

    return uploaded_folder_path


def write_and_extract_zip_file(base64_encoded_zip, work_path):
    zip_file_path = os.path.join(work_path, 'uploaded.zip')

    with open(zip_file_path, 'wb') as fh:
        fh.write(base64.b64decode(base64_encoded_zip))

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(work_path)
