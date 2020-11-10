
from os import stat
from database import (ImageModel, CategoryModel, AnnotationModel, UserModel)
from usecase.importLabelme.addCategoriesToDatasetUseCase import AddCategoriesToDatasetUseCase
from mongoengine import *


class FakeCurrentUser:
    def can_edit(self, category):
        return True

class FakeDataset:
    def __init__(self, id=1):
        self.categories = []
        self.isSave = False
        self.id = id
        self.directory = ""
        
    def categories_should_be(self, expected_categories):
        assert self.categories == expected_categories

    def categories_size_should_be(self, expected_size):
        assert len(self.categories) == expected_size

    def update_categories(self, new_categories):
        self.categories = new_categories

    def save(self):
        self.isSave = True
    
    def save_should_be_called(self):
        return self.isSave == True

    def set_directory(self, directory):
        self.directory = directory

    def set_id(self, id):
        self.id = id
    
    def to_json(self):
        import json
        return json.dumps({
            "_id": self.id
        })
    
    def permissions(self, current_user):
        return "permission1"

class MockAddCategoriesToDatasetUseCase(AddCategoriesToDatasetUseCase):
    def __init__(self):
        self.fake_dataset = FakeDataset()

    def find_dataset_by(self, dataset_id):
        return self.fake_dataset

    def set_fake_dataset_to_return(self, fake_dataset):
        self.fake_dataset = fake_dataset


class MockImage(ImageModel):
    def thumbnail_delete(self):
        pass
    
    @staticmethod
    def delete_all():
        MockImage.objects.delete()

class Mother:

    @staticmethod
    def create_user(username, password):
        user = UserModel(
            username=username,
            password=password
        ).save()
        return user.id

    @staticmethod
    def create_annotation(image_id):
        annotation = AnnotationModel(
            image_id=image_id,
            category_id=0,
            metadata={},
            segmentation=[[1, 2, 3, 4]],
            keypoints=[1, 2, 3, 4],
            isbbox=False
        )
        annotation.save()
        return annotation.id

    @staticmethod
    def create_category():
        category = CategoryModel(
            name="category",
            supercategory="supercategory",
            color="red",
            metadata={},
            keypoint_edges=[],
            keypoint_labels=[],
            keypoint_colors=[],
        )
        category.save()
        return category.id

    @staticmethod
    def find_images_by_dataset_id(dataset_id):
        return ImageModel.objects(dataset_id=dataset_id)

    @staticmethod
    def create_image():
        return Mother.create_image_by('test')

    @staticmethod
    def create_image_by(image_name, dataset_id=1):
        image_model = MockImage(
            dataset_id=dataset_id,
            file_name=image_name,
            width=1300,
            height=1300,
            path='/' + image_name
        )
        image_model.save()
        return image_model.id
 
