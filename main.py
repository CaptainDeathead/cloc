import argparse
import os
from pathlib import Path
from typing import List, Dict

class CLOC:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="cloc (Count LOC) is a terminal utility to easily count lines of code in a file / project.", formatter_class=argparse.RawTextHelpFormatter)
        self.parser.add_argument("path_arg", type=str, help="The path to the file / directory cloc should scan.")
        self.parser.add_argument(
            "--ignore",
            type=str,
            action="extend",
            nargs='+',
            help=(
                "Ignore files or directories matching the given patterns.\n"
                "You can provide multiple patterns at once or repeat the --ignore option.\n"
                "When ignoring specific directories their paths should be relative to the path you ran this with.\n"
                "  i.e. You ran: 'cloc ~/Documents/my_project', then if you wish to ignore a specific directory you should provide it's path relative to the ~/Documents/my_project directory."
                "\nExamples:\n"
                "  --ignore '*.py' 'main.cpp'      # Ignore all .py files and main.cpp\n"
                "  --ignore '*.json'               # Ignore all .json files\n"
                "  --ignore 'my_directory/'        # Ignore a specific directory\n"
                "  --ignore 'my_directory/*'       # Ignore all directories with this name\n"
            )
        )

        self.args = self.parser.parse_args()

        if not os.path.exists(self.args.path_arg):
            print(f"Error: Please enter a valid path!\n")
            self.parser.print_help()
            exit()

        self.path = Path(self.args.path_arg)

        self.calculate_ignore_types()

        self.print_loc()

    def calculate_ignore_types(self) -> None:
        self.ignore_exts = []
        self.ignore_dirs = []
        self.ignore_strict_files = []
        self.ignore_strict_dirs = []

        if self.args.ignore is None: return

        for pattern in self.args.ignore:
            if pattern[:2] == '*.':
                self.ignore_exts.append(pattern[1:])
            elif pattern[-2:] == '/*':
                self.ignore_dirs.append(pattern[:-2])
            elif pattern[-1] == '/':
                self.ignore_strict_dirs.append(self.path.joinpath(pattern[:-1]))
            else:
                self.ignore_strict_files.append(pattern)

    def get_file_loc(self, file_path: Path) -> int:
        path = file_path

        if path.name in self.ignore_strict_files or path.suffix in self.ignore_exts:
            return -1

        with open(path, 'rb') as f:
            return len(f.readlines())

    def get_dir_files_loc(self, path: Path) -> Dict[Path, int]:
        if path in self.ignore_strict_dirs or path.name in self.ignore_dirs:
            return []

        print(f"Exploring: {path}...")

        dir_loc = {}

        for new_path in path.iterdir():
            if new_path.is_file():
                file_loc = self.get_file_loc(new_path)
                
                if file_loc >= 0:
                    dir_loc[new_path] = file_loc
            else:
                dir_files_loc = self.get_dir_files_loc(new_path)

                if dir_files_loc is not None:
                    dir_loc.update(dir_files_loc)

        return dir_loc

    def print_loc(self) -> None:
        if self.path.is_file():
            print(self.get_file_loc(self.path))
        else:
            print(self.get_dir_files_loc(self.path))
            print(sum(self.get_dir_files_loc(self.path).values()))

if __name__ == "__main__":
    cloc = CLOC()