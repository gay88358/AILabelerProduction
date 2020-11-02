
from os import stat
from database import (
    ImageModel, 
    CategoryModel, 
    AnnotationModel, 
    UserModel
)

class Finder:
    @staticmethod
    def find_user_by_id(user_id):
        return UserModel.objects.get(id=user_id)

    @staticmethod
    def find_user():
        return UserModel.objects().first()

    @staticmethod
    def find_all_annotations():
        return AnnotationModel.objects()

    @staticmethod
    def find_annotation_by_image_id(image_id):
        try:
            return AnnotationModel.objects.get(image_id=image_id)
        except:
            return None
            
    @staticmethod
    def find_annotation_list_by_image_id(image_id):
        return AnnotationModel.objects(image_id=image_id)

    @staticmethod
    def find_all_images():
        return ImageModel.objects()

    @staticmethod
    def find_annotations_by_category_id(category_id):
        return AnnotationModel.objects(category_id=category_id)

    @staticmethod
    def find_annotations_by(image_id):
        return AnnotationModel.objects(image_id=image_id)

    @staticmethod
    def find_all_categories():
        return CategoryModel.objects.all()

    @staticmethod
    def find_image_by(image_id):
        return ImageModel.objects.get(id=image_id)

    @staticmethod
    def find_category_by(category_id):
        return CategoryModel.objects.get(id=category_id)
    
    @staticmethod
    def find_annotation_by(annotation_id):
        return AnnotationModel.objects.get(id=annotation_id)
