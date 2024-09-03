from os import listdir, makedirs
from os.path import basename, splitext, join, exists, isfile
from shutil import move

class FileMover:
    def __init__(self, source_dir, destination_dir):
        self.source_dir = source_dir
        self.destination_dir = destination_dir

    def generate_unique_filename(self, file_path):
        file_name, file_ext = splitext(basename(file_path))
        base_name = file_name
        dest_file = join(self.destination_dir, file_name + file_ext)
        counter = 2
        while exists(dest_file):
            dest_file = join(self.destination_dir, f"{base_name} ({counter}){file_ext}")
            counter += 1
        return dest_file

    def move_and_rename_if_exists(self, src_file):
        dest_file = self.generate_unique_filename(src_file)
        move(src_file, dest_file)
        print(f"Moved: {basename(src_file)} to {basename(dest_file)}")

    def move_files(self):
        if not exists(self.destination_dir):
            makedirs(self.destination_dir)

        for file_name in listdir(self.source_dir):
            full_file_name = join(self.source_dir, file_name)
            if isfile(full_file_name):
                self.move_and_rename_if_exists(full_file_name)
        print("All files moved, with renaming if necessary.")

