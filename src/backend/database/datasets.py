
from os import stat
from flask_login import current_user
from mongoengine import *
from config import Config

from .tasks import TaskModel

import os


class DatasetModel(DynamicDocument):
    
    id = SequenceField(primary_key=True)
    name = StringField(required=True, unique=True)
    directory = StringField()
    thumbnails = StringField()
    categories = ListField(default=[])

    owner = StringField(required=True)
    users = ListField(default=[])

    annotate_url = StringField(default="")

    default_annotation_metadata = DictField(default={})

    deleted = BooleanField(default=False)
    deleted_date = DateTimeField()

    @staticmethod
    def find_datasets_by_id_list(dataset_id_list):
        result = []
        for dataset_id in dataset_id_list:  
            dataset = DatasetModel.find_by(dataset_id)
            if dataset is None:
                raise ValueError('dataset is not found by dataset id: '  + str(dataset_id))
            result.append(dataset)
        return result


    @staticmethod
    def delete_by_id(dataset_id):
        try:
            DatasetModel.objects(id=dataset_id).delete()
        except:
            return None


    @staticmethod
    def find_by_name_contain(stripID):
        try:
            return DatasetModel.objects(name__contains=stripID)
        except:
            return None

    @staticmethod
    def find_by_name(dataset_name):
        try:
            return DatasetModel.objects().get(name=dataset_name)
        except:
            return None

    @staticmethod
    def find_by(dataset_id):
        try:
            return DatasetModel.objects.get(id=dataset_id)
        except:
            raise ValueError("Dataset is not found given id" + str(dataset_id))

    def save(self, *args, **kwargs):

        directory = os.path.join(Config.DATASET_DIRECTORY, self.name + '/')
        os.makedirs(directory, mode=0o777, exist_ok=True)

        self.directory = directory
        self.owner = current_user.get_username() if current_user else 'system'

        return super(DatasetModel, self).save(*args, **kwargs)

    def update_categories(self, new_categories):
        self.update(set__categories=new_categories)

    def get_users(self):
        from .users import UserModel
    
        members = self.users
        members.append(self.owner)

        return UserModel.objects(username__in=members)\
            .exclude('password', 'id', 'preferences')

    def import_coco(self, coco_json):

        from workers.tasks import import_annotations

        task = TaskModel(
            name="Import COCO format into {}".format(self.name),
            dataset_id=self.id,
            group="Annotation Import"
        )
        task.save()

        cel_task = import_annotations.delay(task.id, self.id, coco_json)

        return {
            "celery_id": cel_task.id,
            "id": task.id,
            "name": task.name
        }

    def export_coco(self, categories=None, style="COCO"):

        from workers.tasks import export_annotations

        if categories is None or len(categories) == 0:
            categories = self.categories

        task = TaskModel(
            name=f"Exporting {self.name} into {style} format",
            dataset_id=self.id,
            group="Annotation Export"
        )
        task.save()

        cel_task = export_annotations.delay(task.id, self.id, categories)

        return {
            "celery_id": cel_task.id,
            "id": task.id,
            "name": task.name
        }

    def scan(self):

        from workers.tasks import scan_dataset
        
        task = TaskModel(
            name=f"Scanning {self.name} for new images",
            dataset_id=self.id,
            group="Directory Image Scan"
        )
        task.save()
        
        cel_task = scan_dataset.delay(task.id, self.id)

        return {
            "celery_id": cel_task.id,
            "id": task.id,
            "name": task.name
        }

    def is_owner(self, user):

        if user.is_admin:
            return True
        
        return user.username.lower() == self.owner.lower()

    def can_download(self, user):
        return self.is_owner(user)

    def can_delete(self, user):
        return self.is_owner(user)
    
    def can_share(self, user):
        return self.is_owner(user)
    
    def can_generate(self, user):
        return self.is_owner(user)

    def can_edit(self, user):
        return user.username in self.users or self.is_owner(user)
    
    def permissions(self, user):
        return {
            'owner': self.is_owner(user),
            'edit': self.can_edit(user),
            'share': self.can_share(user),
            'generate': self.can_generate(user),
            'delete': self.can_delete(user),
            'download': self.can_download(user)
        }


__all__ = ["DatasetModel"]
