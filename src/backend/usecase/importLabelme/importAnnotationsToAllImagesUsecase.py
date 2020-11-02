import json
from os import stat

from database import ImageModel
from .labelme2coco.labelme2Coco import Labelme2CoCoConverter
from .coco2Instruction.cocoDataParser import CoCoDataParser
from .addAnnotationsToImageUseCase import AddAnnotationsToImageUseCase
from .addCategoriesToDatasetUseCase import AddCategoriesToDatasetUseCase

class Labelme2CoCoDataParser:
    def parse(self, labelme_json_string, image_bound_size):
        coco_json = Labelme2CoCoConverter(image_bound_size).convert(labelme_json_string)
        coco_json_string = json.dumps(coco_json)

        result = CoCoDataParser().parse(coco_json_string)
        return result
    


class ImportAnnotationsToImageUsecase:
    def __init__(self, add_categories_to_dataset_usecase):
        self.add_categories_to_dataset_usecase = add_categories_to_dataset_usecase
        self.add_annotations_to_image_usecase = AddAnnotationsToImageUseCase()
        self.parser = Labelme2CoCoDataParser()

    def execute(self, dataset_id, image_id, labelme_json_string):
        result = self.parser.parse(labelme_json_string, self.get_image_bound_size(image_id))
        category_id_map = self.add_categories_to_dataset_usecase.execute(result.get_category_data_list(), dataset_id, image_id)
        annotation_list = self.add_annotations_to_image_usecase.execute(image_id, category_id_map, result.get_annotation_data_list())
        return annotation_list

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
        self.import_annotations_to(images, dataset_id, labelme_json_string)

    def import_annotations_to(self, images, dataset_id, labelme_json_string):
        for image in images:
            self.import_annotation_to_image.execute(dataset_id, image.id, labelme_json_string)

