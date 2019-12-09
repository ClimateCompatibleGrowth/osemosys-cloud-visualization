import wget
import os, sys
from zipfile import ZipFile

url = 'http://osemosys-cloud.herokuapp.com/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBbVlDIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--ff2f8155703f97ee7f7fe048bf3fd740a1e5fdcf/csv_159.zip?disposition=attachment'
wget.download(url, 'myCsv.zip')
zip_path = os.path.join(os.getcwd(), 'myCsv.zip')
with ZipFile(zip_path, 'r') as zipObj:
    zipObj.extractall('myCsv')

results_path = os.path.join(os.getcwd(), 'myCsv/')
