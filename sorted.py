import os
import shutil
from pathlib import Path
from threading import Thread
from datetime import datetime

extensions = {'video': ['mp4', 'mov', 'avi', 'mkv'],
              'audio': ['mp3', 'wav', 'ogg', 'amr'],
              'images': ['jpg', 'png', 'jpeg', 'svg'],
              'archives': ['zip', 'gz', 'tar'],
              'documents': ['pdf', 'txt', 'doc', 'docx', 'xlsx', 'pptx', 'odt'],
              'others': []
              }

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ#$%&()^+-:;<=>?@[]{|`~}!\\"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_",
               "_", "_", "_",
               "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name):

    new_name = name.translate(TRANS)
    return new_name


def create_folders_from_list(folder_path, folder_names):
    for folder in folder_names:
        try:

            if not os.path.exists(f'{folder_path}/{folder}'):
                os.mkdir(f'{folder_path}/{folder}')

        except FileExistsError:
            pass


file_paths = []
suborder_paths = []


def paths(path, level=1):
    names_dir = os.listdir(path)

    file_paths.extend([f.path for f in os.scandir(path) if not f.is_dir()])

    suborder_paths.extend([f.path for f in os.scandir(path) if f.is_dir()])
    for elem in names_dir:

        if os.path.isdir(path + "/" + elem):
            paths(path + "/" + elem, level + 1)

    return file_paths, suborder_paths


def sort_files(path):

    ext_list = list(extensions.items())

    for file_path in file_paths:
        file_path = str(file_path)
        extension = file_path.split('.')[-1]

        file_name = file_path.split('/')[-1]

        for dict_key_int in range(len(ext_list)):

            if extension in ext_list[dict_key_int][1]:
                shutil.move(file_path, f'{path}/{ext_list[dict_key_int][0]}/{normalize(file_name)}')

    for ar_file in os.listdir(path + "/" + "archives"):
        try:
            shutil.unpack_archive(path + "/" + "archives" + "/" + ar_file, path + "/" + "archives")
            os.remove(path + "/" + "archives" + "/" + ar_file)

        except shutil.ReadError:
            pass

    names_file = [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]
    for unknown_file in names_file:
        shutil.move(path + "/" + unknown_file, path + "/" + "others" + "/" + normalize(unknown_file))


def remove_empty_folders(path, level=1):
    for p in suborder_paths:
        p = str(p)
        if not os.listdir(p):
            try:
                os.rmdir(p)
                remove_empty_folders(path + "/" + p, level + 1)
            except FileNotFoundError:
                pass
def sort():
    try:
        main_path = input("Enter path for folder: ")
        start = datetime.now().timestamp()

        th2 = Thread(target=paths, args=(main_path,))
        th2.start()

        create_folders_from_list(main_path, extensions)
        sort_files(main_path)
        remove_empty_folders(main_path)
        print("Your files are sorted.\n" + "Deleting empty folders")
        for name_dir in os.listdir(main_path):
            print()
            print(f"{name_dir.capitalize()}: ")
            for name_file in os.listdir(main_path + "/" + name_dir):
                print(f"    - {name_file}")
        end = datetime.now().timestamp()
        result = end - start
        print(result)

    except FileNotFoundError:

        print("The path was wronging. Try again")

if __name__ == "__main__":

    th1 = Thread(target=sort)
    th1.start()

