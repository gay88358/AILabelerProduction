import os
from usecase.util.commandHelper import CommandHelper

class FilePathFinder:


    @staticmethod
    def delete_all_contents_in(directory):
        for file_path in FilePathFinder.find_file_path_in(directory):
            result = CommandHelper.execute(['rm', file_path])


    def find_image_file_path_in(self, directory):
        for root, dirs, files in os.walk(directory):
            if root.split('/')[-1].startswith('.'):
                continue
            return self.collect_paths_from(files, root)

    def collect_paths_from(self, files, root):
        result = []
        for file in files:
            path = os.path.join(root, file)
            result.append(path)
        return result
    
    @staticmethod
    def find_file_path_in(directory):
        result = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                result.append(path)
        return result
