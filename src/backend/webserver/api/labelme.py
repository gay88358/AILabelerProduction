
from usecase.importLabelme.datasetRepository import DatasetRepository
from flask_restplus import Namespace, Resource, reqparse
from flask_login import current_user
from flask_restplus import Namespace, Resource, reqparse

from usecase.user.encryptionService import EncryptionService
from usecase.importLabelme.createNewDatasetUsecase import CreateNewDatasetUsecase
from usecase.importLabelme.scanningImagesAndJsonUsecase import ScanningImagesAndJsonUsecase
from usecase.importLabelme.addSharedFolderUsecase import AddSharedFolderUsecase
from usecase.importLabelme.loadDefectCode.defectCodeParser import DefectCodeLoader
from usecase.user.createUserUsecase import CreateUserUsecase

from .userInfo import *
from .common.response import *
from .common.logger import *

import logging
logger = logging.getLogger('gunicorn.error')

class LabelmeRequestParser:
    @staticmethod
    def labelme_create_dataset():
        labelme_create_dataset = reqparse.RequestParser()
        labelme_create_dataset.add_argument('dataset', type=list, required=True, location='json')
        labelme_create_dataset.add_argument('id', type=str, required=True, location='json')
        return labelme_create_dataset

    @staticmethod
    def labelme():
        labelme = reqparse.RequestParser()
        labelme.add_argument('labelme_json', type=dict, required=True, location='json')
        labelme.add_argument('dataset_id', required=True, location='json')
        labelme.add_argument('image_id', location='json')
        return labelme

api = Namespace('labelme', description='labelme operations')

@api.route('/')
class Labelme(Resource):
    @api.expect(LabelmeRequestParser.labelme())
    def post(self):
        return {
            "success": "ok"
        }

@api.route('/defect_code')
class DefectCode(Resource):
    def get(self):
        get_logger().info("DefectCode Loading")
        result = DefectCodeLoader.create()\
            .map(lambda loader: loader.load_defect_code())
        if result.is_success() == False:
            return []
        import json
        return json.dumps(result.value)
        
@api.route('/create')
class LabelmeId(Resource):
    @api.expect(LabelmeRequestParser.labelme_create_dataset())
    def post(self):
        args = LabelmeRequestParser.labelme_create_dataset().parse_args()
        stripID = args['id']
        dataset_names = args['dataset']

        result = DefectCodeLoader.create()\
        .flat_map(lambda _: self.create_user()\
        .flat_map(lambda _: self.add_shared_folder_to_user(stripID, dataset_names)\
        .flat_map(lambda user: self.create_all_dataset(user, stripID)\
        .flat_map(lambda dataset_id_list: self.scanning_images_and_json(dataset_id_list, user)) 
        )))
        return response(result)
      
    def create_user(self):
        username = get_user_name()
        password = get_user_password()
        name = get_name()
        email = get_email()
        return CreateUserUsecase(EncryptionService()).create(username, password, name, email)
  
    def add_shared_folder_to_user(self, stripID, dataset_name_list):
        return AddSharedFolderUsecase(DatasetRepository())\
            .execute(current_user, stripID, dataset_name_list)

    def create_all_dataset(self, user, stripID):
        dataset_name_list = user.get_dataset_name_list_with(stripID)
        return CreateNewDatasetUsecase().create_all_dataset(dataset_name_list)

    def scanning_images_and_json(self, dataset_id_list, user):
        return ScanningImagesAndJsonUsecase()\
            .scanning_images_and_json(
                dataset_id_list, 
                user.get_mount_root()
            )