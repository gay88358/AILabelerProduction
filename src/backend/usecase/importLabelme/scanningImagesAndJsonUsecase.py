from usecase.util.result import Result
from .moveService import MoveService
from .importAnnotationsToAllImagesUsecase import ImportAnnotationsToAllImagesUsecase
from ..util.commandHelper import CommandHelper
from .jsonFileFinder import JsonFileFinder
from .filePathFinder import FilePathFinder
from .labelmeChecker import LabelChecker
from .mountDirectory import format_mount_directory
from database import (
    ImageModel,
    DatasetModel
)

class ImageRepository:    
    def __init__(self):
        self.dataset = None
        
    def create_images_from(self, dataset_id):
        self.set_dataset_by(dataset_id)
        image_file_paths = FilePathFinder().find_image_file_path_in(self.dataset.directory)
        self.create_images_by_path_list(image_file_paths)
        self.create_thumbnail_for_all_images()

    def set_dataset_by(self, dataset_id):
        self.dataset = DatasetModel.find_by(dataset_id)

    def create_images_by_path_list(self, image_file_paths):
        for path in image_file_paths:
            self.create_image_by_path(path)
            
    def create_image_by_path(self, path):
        if path.endswith(ImageModel.PATTERN):
            db_image = ImageModel.objects(path=path).first()
            if db_image is not None:
                raise ValueError('Image Should Not Exist In This Path: ' + path)
            
            try:
                ImageModel.create_from_path(path, self.dataset.id).save()
            except:
                raise ValueError('Create Image Failed Given Path: ' + path + ', Dataset Id: ' + int(self.dataset.id))

    def create_thumbnail_for_all_images(self):
        from workers.tasks.thumbnails import thumbnail_generate_single_image
        [thumbnail_generate_single_image.delay(image.id) for image in ImageModel.objects(regenerate_thumbnail=True).all()]

    def delete_image_in_the(self, dataset):
        self.remove_images_model_in_the(dataset)
        self.remove_image_files_in_the(dataset)

    def remove_images_model_in_the(self, dataset):
        for image in ImageModel.find_images_by_dataset_id(dataset.id):
            image.delete()

    def remove_image_files_in_the(self, dataset):
        for file_path in FilePathFinder.find_file_path_in(dataset.directory):
            result = CommandHelper.execute(['rm', file_path])

class ScanningImagesAndJsonUsecase:
    def __init__(self):
        self.image_repository = ImageRepository()
        
    def scanning_images_and_json(self, dataset_id_list, dataset_source_folder_path):                
        return self.check_labelme_json(dataset_id_list, dataset_source_folder_path) \
            .flat_map(lambda _: self.import_json_to_all_dataset(dataset_id_list, dataset_source_folder_path))

    # traverse api for functional api
    def check_labelme_json(self, dataset_id_list, dataset_source_folder_path):
        for dataset in DatasetModel.find_datasets_by_id_list(dataset_id_list):
            result = format_mount_directory(dataset_source_folder_path, dataset.name)\
                .flat_map(lambda path: self.find_labelme_json(path)\
                .flat_map(lambda labelme_json: LabelChecker.check_string(labelme_json)))
            if result.is_failure():
                return result
        return Result.success('')

    def import_json_to_all_dataset(self, dataset_id_list, dataset_source_folder_path):
        for dataset in DatasetModel.find_datasets_by_id_list(dataset_id_list):
            result = format_mount_directory(dataset_source_folder_path, dataset.name)\
                .flat_map(lambda path: self.execute(dataset.id, path))
            if result.is_failure():
                return result
        return Result.success(dataset_id_list)

    def execute(self, dataset_id, dataset_source_folder_path):
        dataset = DatasetModel.find_by(dataset_id)
        self.move_content_from_source_to_dataset(dataset, dataset_source_folder_path)
        self.image_repository.create_images_from(dataset.id)
        return self.scan_annotation_from_json(dataset_id, dataset_source_folder_path)
        
    def move_content_from_source_to_dataset(self, dataset, dataset_source_folder_path):
        moveService = MoveService(self.image_repository)
        moveService.move_content_from_source_to_dataset(dataset, dataset_source_folder_path)

    def scan_annotation_from_json(self, dataset_id, dataset_source_folder_path):
        return self.find_labelme_json(dataset_source_folder_path)\
            .flat_map(lambda json: self.importAnnotationsToAllImages(dataset_id, json))

    def importAnnotationsToAllImages(self, dataset_id, labelme_json_string):
        usecase = ImportAnnotationsToAllImagesUsecase.create()
        return usecase.execute(dataset_id, labelme_json_string)

    def find_labelme_json(self, dataset_source_folder_path):
        try:
            return Result.success(JsonFileFinder().find_json_in_the(dataset_source_folder_path))
        except ValueError:
            err_msg = 'Decoding json file contained in folder {} has failed, please check the format of json file'.format(dataset_source_folder_path)
            return Result.failure([err_msg])