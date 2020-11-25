import os
from usecase.util.jsonHelper import JsonHelper
from usecase.util.result import Result


class JsonFileFinder:

    def find_label_json_in_the(self, directory):
        if self.is_not_include_label_json(directory):
            err_msg = "Given directory {} must contains Label.json".format(directory)
            return Result.failure([err_msg])

        json_file_path = self.find_json_file_path_in_the(directory)
        return self.load_json_string(json_file_path)
    
    def is_not_include_label_json(self, directory):
        label_json_not_included = self.find_json_file_path_in_the(directory) == ""
        json_file_path = self.find_json_file_path_in_the(directory)
        return not self.is_label_json(json_file_path) or label_json_not_included
    
    def is_label_json(self, directory):
        tokens = directory.split("/")
        file_name = tokens[-1]
        return file_name == "Label.json"

    def load_json_string(self, json_file_path):
        try:
            return Result.success(JsonHelper.load_json_string(json_file_path))
        except ValueError:
            err_msg = 'Decoding json file contained in folder {} has failed, please check the format of json file'.format(json_file_path)
            return Result.failure([err_msg])


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

