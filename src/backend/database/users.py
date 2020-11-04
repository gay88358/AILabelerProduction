import datetime
from sys import hash_info

from mongoengine import *
from flask_login import UserMixin

from .sharedFolder import SharedFolder
from .annotations import AnnotationModel
from .categories import CategoryModel
from .datasets import DatasetModel
from .images import ImageModel

class UserModel(DynamicDocument, UserMixin):

    password = StringField(required=True)
    username = StringField(max_length=25, required=True, unique=True)
    email = StringField(max_length=30)

    name = StringField()
    online = BooleanField(default=False)
    last_seen = DateTimeField()

    is_admin = BooleanField(default=False)

    preferences = DictField(default={})
    permissions = ListField(defualt=[])
    dataset_name_list = ListField(defualt=[])
    # meta = {'allow_inheritance': True}

    @staticmethod
    def user_already_exists(username):
        return UserModel.objects(username__iexact=username).first()
 
    @staticmethod
    def find_by_username(username):
        return UserModel.objects(username=username).first()
        
    @property
    def datasets(self):
        self._update_last_seen()

        if self.is_admin:
            return DatasetModel.objects

        return DatasetModel.objects(Q(owner=self.username) | Q(users__contains=self.username))

    @property
    def categories(self):
        self._update_last_seen()

        if self.is_admin:
            return CategoryModel.objects

        dataset_ids = self.datasets.distinct('categories')
        return CategoryModel.objects(Q(id__in=dataset_ids) | Q(creator=self.username))

    @property
    def images(self):
        self._update_last_seen()

        if self.is_admin:
            return ImageModel.objects

        dataset_ids = self.datasets.distinct('id')
        return ImageModel.objects(dataset_id__in=dataset_ids)

    @property
    def annotations(self):
        self._update_last_seen()

        if self.is_admin:
            return AnnotationModel.objects

        image_ids = self.images.distinct('id')
        return AnnotationModel.objects(image_id__in=image_ids)

    def can_view(self, model):
        if model is None:
            return False

        return model.can_view(self)
    
    def can_download(self, model):
        if model is None:
            return False

        return model.can_download(self)
        
    def can_delete(self, model):
        if model is None:
            return False
        return model.can_delete(self)

    def can_edit(self, model):
        if model is None:
            return False

        return model.can_edit(self)

    def _update_last_seen(self):
        self.update(last_seen=datetime.datetime.utcnow())
    
    def add_shared_folder(self, root, dataset_name_list, mount_root):
        self.__setattr__("root", root)
        self.set_dataset_name_list(dataset_name_list)
        self.__setattr__("mount_root", mount_root)
        self.save()

    def set_dataset_name_list(self, dataset_name_list):
        if len(self.dataset_name_list) > 0:
            new_dataset_name_list = self.dataset_name_list + dataset_name_list
            self.__setattr__("dataset_name_list", new_dataset_name_list)
        else:
            self.__setattr__("dataset_name_list", dataset_name_list)

    def get_shared_folder(self):
        return SharedFolder("", self.dataset_name_list, self.mount_root)

    def get_username(self):
        return self.username
    
    def find_annotation_by_id(self, annotation_id):
        return self.annotations.filter(id=annotation_id).first()

    def find_all_annotations(self):
        return self.annotations.exclude("paper_object").all()


    def find_dataset_by_id(self, dataset_id):
        return self.datasets.filter(id=dataset_id).first()

    def find_all_datasets(self):
        return self.datasets.filter(deleted=False).all()

    def find_exist_dataset_by_id(self, dataset_id):
        return self.datasets.filter(id=dataset_id, deleted=False).first()
    
    def find_all_exist_dataset(self):
        return self.datasets.filter(deleted=False)

    def find_image_by_id(self, image_id):
        return self.images.filter(id=image_id, deleted=False).first()
    
    def find_all_images(self):
        return self.images.filter(deleted=False)

    def find_image_without_deleted_date_by_id(self, image_id):
        return self.images.filter(id=image_id).exclude('deleted_date').first()

    def find_images_by_query(self, query, order):
        return self.images \
        .filter(query) \
        .order_by(order).only('id', 'file_name', 'annotating', 'annotated', 'num_annotations')


    def find_category_by_id(self, category_id):
        return self.categories.filter(id=category_id).first()

    def find_all_categories(self):
        return self.categories.all()

    def find_all_exist_categories(self):
        return self.categories.filter(deleted=False).all()

    def change_preference(self, preference_to_update):
        return self.update(preferences=preference_to_update)

    def get_preferences(self):
        return self.preferences

    def has_admin(self):
        return self.is_admin

    def authenticated(self):
        return self.is_authenticated

    def change_password(self, new_password, generate_password_hash):
        hash_new_password = generate_password_hash(new_password, method='sha256')
        self.update(password=hash_new_password, new=False)

    def is_same_password(self, password, check_password_hash):
        return check_password_hash(self.password, password)

__all__ = ["UserModel"]