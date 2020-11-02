import os
from usecase.util.jsonHelper import JsonHelper



class JsonFileFinder:
    def find_json_in_the(self, directory):
        if self.there_is_no_json_file_contained_in(directory):
            return ""

        json_file_path = self.find_json_file_path_in_the(directory)
        return JsonHelper.load_json_string(json_file_path)

    def find_json_file_path_in_the(self, directory):
        file_path_list = self.get_all_file_path_in_the(directory)
        return self.find_json_file_path(file_path_list)

    def get_all_file_path_in_the(self, directory):
        for root, dirs, file_names in os.walk(directory):
            return list(
                map(
                    lambda name: os.path.join(root, name),
                    file_names
                )
            )
        return []

    def find_json_file_path(self, file_path_list):
        for file_path in file_path_list:
            if self.is_json_file(file_path):
                return file_path
        return ""

    def is_json_file(self, file_path):
        path_tokens = str.split(file_path, '/')
        file_format = path_tokens[-1]
        return '.json' in file_format

    def there_is_no_json_file_contained_in(self, directory):
        if self.find_json_file_path_in_the(directory) == "":
            return True
        return False
