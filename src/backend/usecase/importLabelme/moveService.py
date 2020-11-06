from .filePathFinder import FilePathFinder
from ..util.commandHelper import CommandHelper

class MoveService:
    def __init__(self, image_repository):
        self.image_repository = image_repository

    def move_content_from_source_to_dataset(self, dataset, dataset_source_folder_path):
        self.clear_image_files_in_dataset(dataset)
        self.copy_files_from_source_to(dataset, dataset_source_folder_path)

    def clear_image_files_in_dataset(self, dataset):
        self.image_repository.delete_image_in_the(dataset)

    def copy_files_from_source_to(self, dataset, dataset_source_folder_path):
        for file_path in self.find_file_paths(dataset_source_folder_path):
            result = CommandHelper.execute(['cp', '-r', file_path, dataset.directory])
        # post condition
        self.check_copy_success(dataset, dataset_source_folder_path)
    
    def check_copy_success(self, dataset, dataset_source_folder_path):
        source_content_length = len(self.find_file_paths(dataset_source_folder_path))
        dataset_content_length = len(self.find_file_paths(dataset.directory))
        if source_content_length != dataset_content_length:
            raise ValueError("Source folder location not found, so that can not copy content from source to dataset")

    def find_file_paths(self, path):
        return FilePathFinder.find_file_path_in(path)