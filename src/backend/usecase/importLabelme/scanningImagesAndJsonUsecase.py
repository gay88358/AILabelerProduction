from usecase.util.result import Result
from .moveService import MoveService
from .importAnnotationsToAllImagesUsecase import ImportAnnotationsToAllImagesUsecase
from ..util.commandHelper import CommandHelper
from .jsonFileFinder import JsonFileFinder
from .filePathFinder import FilePathFinder

from database import (
    ImageModel,
    DatasetModel
)

class ImageRepository:    
    def __init__(self):
        self.dataset = None

    def delete_image_in_the(self, dataset):
        self.remove_images_model_in_the(dataset)
        for file_path in FilePathFinder.find_file_path_in(dataset.directory):
            result = CommandHelper.execute(['rm', file_path])

    def remove_images_model_in_the(self, dataset):
        images = ImageModel.objects(dataset_id=dataset.id)
        for image in images:
            image.thumbnail_delete()
            image.delete()

    def create_images_from(self, dataset_id):
        self.set_dataset_by(dataset_id)
        image_file_paths = FilePathFinder().find_image_file_path_in(self.dataset.directory)
        self.create_images_by_path_list(image_file_paths)
        self.create_thumbnail_for_all_images()

    def create_images_by_path_list(self, image_file_paths):
        for path in image_file_paths:
            self.create_image_by_path(path)

    def set_dataset_by(self, dataset_id):
        self.dataset = self.find_dataset_by(dataset_id)

    def find_dataset_by(self, dataset_id):
        return DatasetModel.objects.get(id=dataset_id)

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

class ScanningImagesAndJsonUsecase:
    def __init__(self):
        self.image_repository = ImageRepository()
        
    def scanning_images_and_json(self, dataset_id_list, dataset_source_folder_path):
        for dataset_id in dataset_id_list:  
            dataset = DatasetModel.find_by(dataset_id)
            if dataset is None:
                raise ValueError('dataset is not found by dataset id: '  + str(dataset_id))
            
            self.execute(dataset_id, dataset_source_folder_path + '/' + dataset.name)
        return Result.success(dataset_id_list)

    def execute(self, dataset_id, dataset_source_folder_path):
        dataset = DatasetModel.find_by(dataset_id)
        self.move_content_from_source_to_dataset(dataset, dataset_source_folder_path)
        self.image_repository.create_images_from(dataset.id)
        self.scan_annotation_from_json(dataset_id, dataset_source_folder_path)

    def move_content_from_source_to_dataset(self, dataset, dataset_source_folder_path):
        moveService = MoveService(self.image_repository)
        moveService.move_content_from_source_to_dataset(dataset, dataset_source_folder_path)

    def scan_annotation_from_json(self, dataset_id, dataset_source_folder_path):
        labelme_json_string = JsonFileFinder().find_json_in_the(dataset_source_folder_path)
        usecase = ImportAnnotationsToAllImagesUsecase.create()
        usecase.execute(dataset_id, labelme_json_string)
