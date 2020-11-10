

from database import (
    ImageModel,
    AnnotationModel,
    CategoryModel,
    DatasetModel
)
from usecase.util.result import Result

import shutil

class DatasetRepository:
    def __init__(self):
        pass

    def delete_by_stripId(self, stripId):
        if self.find_datasets_by_stripID(stripId) == None:
            err_msg = 'Given stripId {} is invalid'.format(stripId)
            return Result.failure([err_msg])

        for d in self.find_datasets_by_stripID(stripId):
            self.delete(d)
        return Result.success(stripId)

    def find_datasets_by_stripID(self, stripId):
        key = stripId + "/"
        return DatasetModel.find_by_name_contain(key)
            
    def delete(self, dataset):
        self.delete_all_images(dataset)
        self.delete_dataset(dataset)

    def delete_dataset(self, dataset):
        DatasetModel.delete_by_id(dataset.id)
        self.delete_whole_directory(dataset)

    def delete_whole_directory(self, dataset):
        shutil.rmtree(dataset.directory)

    def delete_all_images(self, dataset):
        images = self.find_images_in(dataset)
        for image in images:
            image.delete()

    def find_images_in(self, dataset):
        images = ImageModel.find_images_by_dataset_id(dataset.id)
        return images