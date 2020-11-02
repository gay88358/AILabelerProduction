
from flask_restplus import reqparse

class Parser:
    @staticmethod
    def update_dataset_parser():
        update_dataset = reqparse.RequestParser()
        update_dataset.add_argument('categories', location='json', type=list, help="New list of categories")
        update_dataset.add_argument('default_annotation_metadata', location='json', type=dict,
                                    help="Default annotation metadata")                            
        return update_dataset

    @staticmethod
    def create_dataset_parser():
        dataset_create = reqparse.RequestParser()
        dataset_create.add_argument('name', required=True)
        dataset_create.add_argument('categories', type=list, required=False, location='json',
                                    help="List of default categories for sub images")
        return dataset_create