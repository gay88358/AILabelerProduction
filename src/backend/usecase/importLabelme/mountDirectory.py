import os
from usecase.util.result import Result

def format_mount_directory(mount_directory, dataset_name):
    path = mount_directory + "/" + dataset_name
    if os.path.isdir(path) == False:
        error_message = '{} is not a valid directory, please check given id and dataset parameter'.format(path)
        return Result.failure([error_message])
    return Result.success(path)
