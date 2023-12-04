import os

def extract_filename_from_path(path):
    filename = os.path.basename(path).split('.')[0]
    return filename

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_dir_if_not_exist(dir_name):
    is_exist = os.path.exists(dir_name)
    if not is_exist:
        os.makedirs(dir_name)