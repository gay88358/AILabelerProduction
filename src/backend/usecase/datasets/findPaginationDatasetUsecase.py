

from database import DatasetModel
from database import ImageModel

from .pagination import Pagination
import json


class FindPaginationDatasetUsecase:
    
    def execute(self, limit, page, stripID, current_user):
        datasets = self.find_datasets_by(stripID)

        pagination = self.create_pagination(len(datasets), limit, page)
        
        datasets = self.split_dataset_by(pagination, datasets)
        
        datasets_json = self.to_datasets_json(datasets, current_user)

        return {
            "pagination": pagination.export(),
            "datasets": datasets_json,
        }

    def create_pagination(self, datasets_length, limit, page):
        return Pagination(datasets_length, limit, page)

    def split_dataset_by(self, pagination, datasets):
        return datasets[pagination.start:pagination.end]

    def to_datasets_json(self, datasets, current_user):
        datasets_json = []
        for dataset in datasets:
            dataset_json = self.fix_ids(dataset)
            images = ImageModel.objects(dataset_id=dataset.id, deleted=False)
            dataset_json['numberImages'] = images.count()
            dataset_json['numberAnnotated'] = images.filter(annotated=True).count()
            dataset_json['permissions'] = dataset.permissions(current_user)
            first = images.first()
            if first is not None:
                dataset_json['first_image_id'] = images.first().id
            datasets_json.append(dataset_json)
        return datasets_json

    def fix_ids(self, objs):
        objects_list = json.loads(objs.to_json().replace('\"_id\"', '\"id\"'))
        return objects_list

    def find_datasets_by(self, stripID):
            # contain bugs, id need to 123/ exactly
        key = stripID + "/"
        return DatasetModel.find_by_name_contain(key)

        # datasets = list(
        #     map(
        #         lambda name: DatasetModel.find_by_name(name),
        #         stripID
        #     )
        # )
        # return datasets