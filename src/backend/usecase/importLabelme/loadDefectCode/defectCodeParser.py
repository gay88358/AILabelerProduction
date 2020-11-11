import os
from usecase.util.jsonHelper import JsonHelper
from usecase.util.result import Result

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
            lambda l: self.create_defect_code_dict(l),
            labels
        ))

    def create_defect_code_dict(self, label):
        defect_code_dict = {}
        defect_code_dict['Defect_Code'] = label['Defect_Code']
        defect_code_dict['Vim300_Code'] = label['Vim300_Code']
        return defect_code_dict

class DefectCodeLoader:
    @staticmethod
    def create():
        try:
            return Result.success(DefectCodeLoader())
        except FileNotFoundError as e:
            return Result.failure(['Please put label_map.json into root folder'])

    def __init__(self):
        self.json_document = self.load_json_document()

    def load_json_document(self):
        defect_code_file_path = "/worksapce/sharedFolder/ATWEX/label_map.json"
        json_document = JsonHelper.load_json_document(defect_code_file_path)
        return json_document
            
    def load_defect_code(self):        
        defect_code = DefectCodeParser(self.json_document)
        return defect_code.to_defect_code_catalog()
