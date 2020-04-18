import os
import shutil
import pathlib
import re
from config import ROOT
from constants import folder_names, file_extentions


def with_path(name: str, path=ROOT) -> str:
    return os.path.join(path, name)


def folder_to_move(ext: str) -> str:
    for folder_name, file_ext in file_extentions.items():
        if ext.lower() in file_ext:
            return with_path(folder_name)
    return with_path('Misc')


def move_to_folder(file_path: str, file_name: str, folder_to_move: str, called_n: int = 1):
    path_to_move = with_path(folder_to_move)
    full_file_path = with_path(file_name, file_path)
    if not os.path.isdir(path_to_move):
        pathlib.Path(path_to_move).mkdir(parents=True, exist_ok=True)
    elif os.path.isfile(with_path(file_name, path_to_move)):
        search_pattern = r'(.*)(\(\d\))\.(.*)' if called_n > 1 else r'(.*)\.(.*)'
        d = re.search(search_pattern, file_name)
        ext = d.group(3) if called_n > 1 else d.group(2)
        new_name = d.group(1) + f'({called_n}).' + ext
        shutil.move(full_file_path, with_path(new_name, file_path))
        move_to_folder(file_path, new_name, folder_to_move, called_n + 1)
    else:
        shutil.move(full_file_path, with_path(file_name, folder_to_move))


def main():
    for (path, dirs, files) in os.walk(ROOT):
        if path.split('/')[-1] not in folder_names:
            for file in files:
                ext = file.split('.')[-1]
                if ext not in ['py', 'pyc']:
                    move_to_folder(path, file, folder_to_move(ext))


if __name__ == "__main__":
    main()
