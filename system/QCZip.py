import os
from zipfile import ZipFile


def extract_qc_zip(zip_path, files, new_path):
    """
    Extract a single file insize a fastqc zip
    :param zip_path: path to the zip file
    :param files: iterable of items to be extracted from the zip
    :param new_path: path where the item will be extracted
    """
    identity = zip_path[zip_path.rfind('\\')+1: -4]
    file_loc = identity + "/"
    with ZipFile(zip_path) as my_zip:
        for file in files:
            my_zip.extract(file_loc + file, path=new_path)
            os.rename(new_path+"/"+identity+"/"+file, new_path+"/"+identity+file[file.rfind("."):])
        os.removedirs(new_path+"/"+identity)


def extract_dir(dir, files=("fastqc_data.txt", "fastqc_report.html"), new_path=""):
    """
    Extract all zip files in the directory
    :param dir: Directory of all the zip files
    :param files: iterable of items that will be extracted from each zip file
    :param new_path: path to where the extracted items will be placed
    """
    for filename in os.listdir(dir):
        if filename.endswith(".zip"):
            extract_qc_zip(os.path.join(dir, filename), files, new_path)
        else:
            continue


dir_path = "C:\\Users\\shikd\\Google Drive\\ByteSize\\20170712"
extract_path = "C:\\Users\\shikd\\Google Drive\\ByteSize\\20170712\\extracted"
extract_dir(dir_path, new_path=extract_path)
