
from usecase.exportLabelme.exportLabelmeUsecase import ExportLabelmeUsecase
from flask_restplus import Namespace, Resource
from flask_login import login_required, current_user
from flask import request
from ..util import query_util, coco_util, profile, thumbnails
from usecase.util.jsonHelper import JsonHelper
import json
from workers.tasks.jsonFileFinder import JsonFileFinder


from config import Config
from database import (
    ImageModel,
    CategoryModel,
    AnnotationModel,
)

from usecase.saveAggregateData.saveAllAggregateDataUsecase import SaveAllAggregateDataUsecase

api = Namespace('annotator', description='Annotator related operations')


class AggregateData:
    def __init__(self, json_data):
        self.json_data = json_data

    def get_dataset_name(self):
        return self.json_data['dataset']['name']

    def get_image_id(self):
        return self.json_data['image']['id']
    
    def get_stripID(self):
        return self.json_data['stripID']

@api.route('/data')
class AnnotatorData(Resource):

    @profile
    @login_required
    def post(self):
        """
        Called when saving data from the annotator client
        """
        # encapsulate incoming datastructure to aggregate object
        # prevent data structure information from cluterring codebase
        aggregate = AggregateData(request.get_json(force=True))
        
        self.save_aggregate_data(aggregate)

        labelme_document = self.convert_labelme_from_database(aggregate)

        self.write_back_to_shared_folder(labelme_document, aggregate)

        return labelme_document
    
    def save_aggregate_data(self, aggregate):
        assert current_user is not None
        SaveAllAggregateDataUsecase().execute(
            aggregate.json_data, 
            current_user
        )

    def convert_labelme_from_database(self, aggregate):
        usecase = ExportLabelmeUsecase()
        return usecase.execute(aggregate.get_image_id())

    def write_back_to_shared_folder(self, labelme_document, aggregate):
        file_directory = current_user.get_shared_folder_with(aggregate.get_stripID()).get_mount_directory(aggregate.get_dataset_name())
        json_file_finder = JsonFileFinder()
        json_file_size = json_file_finder.json_file_size(file_directory)
        if json_file_size > 1 or json_file_size == 0:
            err_msg = "Dataset folder {} can contain atmost one json file, please remove redundant json file or add json file".format(file_directory)
            raise ValueError(err_msg)
        json_file_path = json_file_finder.find_json_file_path_in_the(file_directory)
        JsonHelper.replace_document(json_file_path, labelme_document)

@api.route('/data/<int:image_id>')
class AnnotatorId(Resource):

    @profile
    @login_required
    def get(self, image_id):
        """ Called when loading from the annotator client """
        image = ImageModel.objects(id=image_id)\
            .exclude('events').first()

        if image is None:
            return {'success': False, 'message': 'Could not load image'}, 400
        
        dataset = current_user.find_dataset_by_id(image.dataset_id)
        if dataset is None:
            return {'success': False, 'message': 'Could not find associated dataset'}, 400

        categories = CategoryModel.objects(deleted=False)\
            .in_bulk(dataset.categories).items()

        # Get next and previous image
        images = ImageModel.objects(dataset_id=dataset.id, deleted=False)
        pre = images.filter(file_name__lt=image.file_name).order_by('-file_name').first()
        nex = images.filter(file_name__gt=image.file_name).order_by('file_name').first()

        preferences = {}
        if not Config.LOGIN_DISABLED:
            preferences = current_user.get_preferences()
        # Generate data about the image to return to client
        data = {
            'image': query_util.fix_ids(image),
            'categories': [],
            'dataset': query_util.fix_ids(dataset),
            'preferences': preferences,
            'permissions': {
                'dataset': dataset.permissions(current_user),
                'image': image.permissions(current_user)
            }
        }

        data['image']['previous'] = pre.id if pre else None
        data['image']['next'] = nex.id if nex else None

        for category in categories:
            category = query_util.fix_ids(category[1])

            category_id = category.get('id')
            annotations = AnnotationModel.objects(image_id=image_id, category_id=category_id, deleted=False)\
                .exclude('events').all()

            category['show'] = True
            category['visualize'] = False
            category['annotations'] = [] if annotations is None else query_util.fix_ids(annotations)
            data.get('categories').append(category)

        return data


