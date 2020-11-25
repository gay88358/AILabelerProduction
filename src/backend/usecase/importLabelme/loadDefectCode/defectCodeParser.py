from usecase.util.jsonHelper import JsonHelper
from usecase.util.result import Result


class Label:
    def __init__(self, label_document):
        self.label_document = label_document
        
    def get_category_name(self):
        return self.label_document['Label_Catagory']

    def get_defect_code(self):
        return self.label_document['Defect_Code']
    
    def get_vim_300_code(self):
        return self.label_document['Vim300_Code']

class LabelMap:
    def __init__(self, label_map_document):
        self.labels = self.to_label_model_list(label_map_document)
    
    def to_label_model_list(self, label_map_document):
        return list(
                map(
                    lambda label_document: Label(label_document),
                    label_map_document['Label']
                )
            )
    
    def find_unique_category_name(self):
        category_name_list = list(map(
            lambda l: l.get_category_name(),
            self.labels
        ))
        return self.remove_duplicate(category_name_list)

    def remove_duplicate(self, category_name_list):
        result = []
        for category_name in category_name_list:
            if category_name not in result:
                result.append(category_name)
        return result

    def find_labels_by(self, category_name):
        return list(
            filter(
                lambda l: l.get_category_name() == category_name,
                self.labels
            )
        )

class DefectCodeParser:
    def __init__(self, label_map_document):
        self.label_map = LabelMap(label_map_document)

    def to_defect_code_catalog(self):
        result = {}

        result['defectcode_catalog'] = list(
            map(
                lambda name: self.create_defect_code(name),
                self.label_map.find_unique_category_name()
            )
        )
        return result

    def create_defect_code(self, category_name):
        return {
            'category_name': category_name,
            'category_id': 0,
            'defect_code_list':  self.find_defect_code_list(category_name)
        }

    def find_defect_code_list(self, category_name):
        labels = self.label_map.find_labels_by(category_name)
        return self.extract_defect_code_and_vim_300_from(labels)

    def extract_defect_code_and_vim_300_from(self, labels):
        return list(map(
            lambda l: self.extract_defect_code_and_vim_300(l),
            labels
        ))

    def extract_defect_code_and_vim_300(self, label):
        result = {}
        result['Defect_Code'] = label.get_defect_code()
        result['Vim300_Code'] = label.get_vim_300_code()
        return result
    

class DefectCodeLoader:
    @staticmethod
    def create():
        try:
            return Result.success(DefectCodeLoader())
        except FileNotFoundError as e:
            return Result.failure(['Please put label_map.json into root folder'])
        except ValueError as e:
            return Result.failure(['The format of given label_map.json is invalid, please check and fix the format of json file'])

    def __init__(self):
        self.json_document = self.load_json_document()

    def load_json_document(self):
        defect_code_file_path = "/worksapce/sharedFolder/ATWEX/label_map.json"
        json_document = JsonHelper.load_json_document(defect_code_file_path)
        return json_document

    def load_defect_code(self):        
        defect_code = DefectCodeParser(self.json_document)
        return defect_code.to_defect_code_catalog()
