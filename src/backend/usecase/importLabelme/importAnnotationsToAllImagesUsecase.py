import json
from os import stat

from database import ImageModel
from .labelme2coco.labelme2Coco import Labelme2CoCoConverter
from .coco2Instruction.cocoDataParser import CoCoDataParser
from .addAnnotationsToImageUseCase import AddAnnotationsToImageUseCase
from .addCategoriesToDatasetUseCase import AddCategoriesToDatasetUseCase
from usecase.util.result import Result

class Labelme2CoCoDataParser:
    def parse(self, labelme_json_string, image_bound_size):
        return self.labelme2coco(labelme_json_string, image_bound_size)\
            .flat_map(lambda coco_json_string: self.coco2cocoData(coco_json_string))
    
    def labelme2coco(self, labelme_json_string, image_bound_size):
        try:
            coco_json = Labelme2CoCoConverter(image_bound_size).convert(labelme_json_string)
            coco_json_string = json.dumps(coco_json)
            return Result.success(coco_json_string)
        except:
            return Result.failure(['The point of shape in labelme.json is out of image bound size'])
    
    def coco2cocoData(self, coco_json_string):
        return Result.success(CoCoDataParser().parse(coco_json_string))

class ImportAnnotationsToImageUsecase:
    def __init__(self, add_categories_to_dataset_usecase):
        self.add_categories_to_dataset_usecase = add_categories_to_dataset_usecase
        self.add_annotations_to_image_usecase = AddAnnotationsToImageUseCase()
        self.parser = Labelme2CoCoDataParser()

    def execute(self, dataset_id, image_id, labelme_json_string):
        return self.parser\
            .parse(labelme_json_string, self.get_image_bound_size(image_id))\
            .flat_map(lambda parseResult: self.add_categories_and_annotation(dataset_id, image_id, parseResult))
    
    def add_categories_and_annotation(self, dataset_id, image_id, parseResult):
        category_data_list = parseResult.get_category_data_list()
        annotation_data_list = parseResult.get_annotation_data_list()
        category_id_map = self.add_categories_to_dataset_usecase.execute(category_data_list, dataset_id, image_id)
        annotation_list = self.add_annotations_to_image_usecase.execute(image_id, category_id_map, annotation_data_list)
        return Result.success(annotation_list)
    
    def get_image_bound_size(self, image_id):
        image = ImageModel.find_by(image_id)
        return image.get_image_bound_size()

class ImportAnnotationsToAllImagesUsecase:
    @staticmethod
    def create_by(add_categories_to_dataset):
        return ImportAnnotationsToAllImagesUsecase( 
            ImportAnnotationsToImageUsecase( # import annotation to one image
                add_categories_to_dataset# dependency injection
            )
        )
    
    @staticmethod
    def create_with_import_annotation(import_annotations_to_image):
        return ImportAnnotationsToAllImagesUsecase( 
            import_annotations_to_image
        )

    @staticmethod
    def create():
        return ImportAnnotationsToAllImagesUsecase( 
            ImportAnnotationsToImageUsecase( # import annotation to one image
                AddCategoriesToDatasetUseCase() # dependency injection
            )
        )

    def __init__(self, import_annotation_to_image):
        self.import_annotation_to_image = import_annotation_to_image

    def execute(self, dataset_id, labelme_json_string):
        images = ImageModel.find_images_by_dataset_id(dataset_id)
        return self.import_annotations_to(images, dataset_id, labelme_json_string)

    def import_annotations_to(self, images, dataset_id, labelme_json_string):
        for image in images:
            result = self.import_annotation_to_image.execute(dataset_id, image.id, labelme_json_string)
            if result.is_failure():
                return result
        return Result.success(dataset_id)
