
import json


from usecase.util.jsonHelper import JsonHelper


from ..utility.usecaseFixture import (
    mongo_connection_setup
)

from ..utility.findHelper import (
    Finder
)

from ..utility.objectMother import (
    FakeDataset, Mother, FakeCurrentUser
)

class DefectCode:
    def __init__(self, defect_code_document):
        self.labels = defect_code_document['Label']

    def defect_code_list(self, category_name):
        labels_with_same_category_name = self.find_labels_by_category_name(category_name)
        return self.to_defect_code_list(labels_with_same_category_name)

    def find_labels_by_category_name(self, category_name):
        return list(filter(
            lambda l: l['Label_Catagory'] == category_name,
            self.labels
        ))
    
    def find_all_distinct_category_name(self):
        category_name_list = list(map(
            lambda l: l['Label_Catagory'],
            self.labels
        ))
        return set(category_name_list)

    def to_defect_code_list(self, labels):
        return list(map(
            lambda l: l['Defect_Code'],
            labels
        ))
    
    def to_defect_code_catalog(self):
        result = {}
        result['defectcode_catalog'] = []
        for name in self.find_all_distinct_category_name():
            defect_code_token = {
                'category_name': name,
                'category_id': 0,
                'defect_code_list':  set(self.defect_code_list(name))
            }
            result['defectcode_catalog'].append(defect_code_token)
        return result

class TestCase:
    
    def test_convert_to_defect_code_catalog(self):
        # Arrange
        defect_code = DefectCode(self.load_defect_json_document())
        # Act
        catalog = defect_code.to_defect_code_catalog()
        # Assert
        assert len(catalog['defectcode_catalog']) == 4

    def load_defect_json_document(self):
        json_str = JsonHelper.load_json_string("/Users/koushiken/Desktop/coco-annotator-0.11.1/backend/sharedFolder/defectcode.json")
        json_document = json.loads(json_str)
        return json_document