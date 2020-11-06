
from usecase.util.result import Result
from flask_restplus import Namespace, Resource, reqparse
from flask_login import current_user
from flask_restplus import Namespace, Resource, reqparse

from usecase.user.encryptionService import EncryptionService
from usecase.importLabelme.createNewDatasetUsecase import CreateNewDatasetUsecase
from usecase.importLabelme.scanningImagesAndJsonUsecase import ScanningImagesAndJsonUsecase
from usecase.importLabelme.addSharedFolderUsecase import AddSharedFolderUsecase

from usecase.user.createUserUsecase import CreateUserUsecase

from usecase.util.jsonHelper import JsonHelper


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

class DefectCodeParser:
    def __init__(self, defect_code_document):
        self.labels = defect_code_document['Label']

    def to_defect_code_catalog(self):
        result = {}

        result['defectcode_catalog'] = list(
            map(
                lambda name: self.create_defect_code_token(name),
                self.find_all_distinct_category_name()
            )
        )
        return result

    def find_all_distinct_category_name(self):
        category_name_list = list(map(
            lambda l: l['Label_Catagory'],
            self.labels
        ))
        return list(set(category_name_list))

    def create_defect_code_token(self, category_name):
        return {
            'category_name': category_name,
            'category_id': 0,
            'defect_code_list':  self.find_defect_code_list(category_name)
        }

    def find_defect_code_list(self, category_name):
        labels_with_same_category_name = self.find_labels_by_category_name(category_name)
        return self.to_defect_code_list(labels_with_same_category_name)

    def find_labels_by_category_name(self, category_name):
        return list(filter(
            lambda l: l['Label_Catagory'] == category_name,
            self.labels
        ))
    
    def to_defect_code_list(self, labels):
        return list(map(
            lambda l: l['Defect_Code'],
            labels
        ))
    
@api.route('/defect_code')
class DefectCode(Resource):
    def get(self):
        defect_code_file_path = "/worksapce/sharedFolder/ATWEX/defectcode.json"
        json_document = JsonHelper.load_json_document(defect_code_file_path)

        defect_code = DefectCodeParser(json_document)
        
        return defect_code.to_defect_code_catalog()

@api.route('/create')
class LabelmeId(Resource):
    @api.expect(LabelmeRequestParser.labelme_create_dataset())
    def post(self):
        args = LabelmeRequestParser.labelme_create_dataset().parse_args()
        stripID = args['id']
        dataset_names = args['dataset']

        result = self.create_user()\
        .flat_map(lambda _: self.add_shared_folder_to_user(stripID, dataset_names)\
        .flat_map(lambda user: self.create_all_dataset(user)\
        .flat_map(lambda dataset_id_list: self.scanning_images_and_json(dataset_id_list, user, stripID)) 
        ))
        return self.response(result)
      
    def create_user(self):
        username = "WebUILabeler"
        password = "webUILabeler"
        name = "webUI"
        email = "gay88358@yahoo.com.tw"
        return CreateUserUsecase(EncryptionService()).create(username, password, name, email)
  
    def add_shared_folder_to_user(self, stripID, dataset_name_list):
        return AddSharedFolderUsecase()\
            .execute(current_user, stripID, dataset_name_list)
        # docker_mount_directory = "/worksapce/sharedFolder/ATWEX" 
        # current_user.add_shared_folder("", dataset_name_list, docker_mount_directory)
        # return Result.success(current_user)

    def create_all_dataset(self, user):
        dataset_name_list = user.get_dataset_name_list()
        return CreateNewDatasetUsecase().create_all_dataset(dataset_name_list)
    
    def scanning_images_and_json(self, dataset_id_list, user, stripID):
        return ScanningImagesAndJsonUsecase()\
            .scanning_images_and_json(
                dataset_id_list, 
                user.get_shared_folder().mount_root
            )

    def response(self, result):
        if result.is_success():
            return self.success(result)
        else:
            return self.error(result)

    def error(self, result):
        return {
                "state": False,
                "code": 400,
                "message": result.error_messages(),
                "result": ""
        }

    def success(self, result):
        return {
                "state": True,
                "code": 200,
                "message": "create success",
                "result": result.value
        }
        
    