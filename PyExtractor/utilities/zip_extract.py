import zipfile

def zip_extract(zip_path, dest_path):
    zip_ref = zipfile.ZipFile(zip_path, 'r')
    zip_ref.extractall(dest_path)
    zip_ref.close()