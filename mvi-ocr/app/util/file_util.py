import os
import shutil

class FileUtil:
    def __init__(self):
        print('FileUtil Class init')

    def copy_file(self, source, destination, file, is_copy):
        if not os.path.exists(destination):
            os.makedirs(destination)

        if is_copy:
            shutil.copyfile(os.path.join(source, file), os.path.join(destination, file))
            return
        shutil.move(os.path.join(source, file), os.path.join(destination, file))
