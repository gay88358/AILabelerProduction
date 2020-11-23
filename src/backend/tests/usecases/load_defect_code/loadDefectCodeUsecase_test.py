
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
        return {
	"Label":[
		{
			"Defect_Code": "First Bond Normal",
			"Vim300_Code": 0,
			"Vision_Defect_Code": 0,
			"Label_Class": 0,
			"Is_Good": 0,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Missing Bond",
			"Vim300_Code": 1004,
			"Vision_Defect_Code": 1,
			"Label_Class": 1,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Broken Wire",
			"Vim300_Code": 1005,
			"Vision_Defect_Code": 2,
			"Label_Class": 2,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Ball Placement",
			"Vim300_Code": 1003,
			"Vision_Defect_Code": 3,
			"Label_Class": 3,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Ball Off Pad",
			"Vim300_Code": 1006,
			"Vision_Defect_Code": 4,
			"Label_Class": 4,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Ball Distance Error",
			"Vim300_Code": 1007,
			"Vision_Defect_Code": 5,
			"Label_Class": 5,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Wire Distance Error",
			"Vim300_Code": 1008,
			"Vision_Defect_Code": 6,
			"Label_Class": 6,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Ball Quality",
			"Vim300_Code": 1014,
			"Vision_Defect_Code": 7,
			"Label_Class": 7,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Ball Undersize",
			"Vim300_Code": 1002,
			"Vision_Defect_Code": 8,
			"Label_Class": 8,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Ball Oversize",
			"Vim300_Code": 1001,
			"Vision_Defect_Code": 9,
			"Label_Class": 9,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 10,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 11,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Ellipse Ratio Error",
			"Vim300_Code": 1012,
			"Vision_Defect_Code": 12,
			"Label_Class": 10,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Lifted Ball",
			"Vim300_Code": 1010,
			"Vision_Defect_Code": 13,
			"Label_Class": 11,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Golf Ball",
			"Vim300_Code": 1011,
			"Vision_Defect_Code": 14,
			"Label_Class": 12,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 15,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 16,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 17,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 18,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 19,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 20,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 21,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 22,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 23,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 24,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 25,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 26,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 27,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 28,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 29,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Twisted Neck",
			"Vim300_Code": 1013,
			"Vision_Defect_Code": 30,
			"Label_Class": 13,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "First Bond Wire Over Shooting",
			"Vim300_Code": 1015,
			"Vision_Defect_Code": 31,
			"Label_Class": 14,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 32,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 33,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Confirm Later",
			"Vim300_Code": 1190,
			"Vision_Defect_Code": 255,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "ball",
			"Catagory_ID": 2,
			"Colour": [
				[0, 0, 0]
			]
		},
		{
			"Defect_Code": "Second Bond Normal",
			"Vim300_Code": 0,
			"Vision_Defect_Code": 0,
			"Label_Class": 0,
			"Is_Good": 0,
			"Label_Catagory": "wedge",
			"Catagory_ID": 3,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Second Bond Missing Weld",
			"Vim300_Code": 1050,
			"Vision_Defect_Code": 1,
			"Label_Class": 1,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 3,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Second Bond Broken Wire",
			"Vim300_Code": 1051,
			"Vision_Defect_Code": 2,
			"Label_Class": 2,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 3,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Second Bond Missing Weld",
			"Vim300_Code": 1050,
			"Vision_Defect_Code": 3,
			"Label_Class": 1,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 3,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Second Bond Weld ACC",
			"Vim300_Code": 1054,
			"Vision_Defect_Code": 4,
			"Label_Class": 4,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 3,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Second Bond Width Rejection",
			"Vim300_Code": 8888,
			"Vision_Defect_Code": 5,
			"Label_Class": 5,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 3,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Second Bond Length Rejection",
			"Vim300_Code": 8888,
			"Vision_Defect_Code": 6,
			"Label_Class": 6,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 3,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Second Bond Weld Clearance Error",
			"Vim300_Code": 1052,
			"Vision_Defect_Code": 7,
			"Label_Class": 7,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 3,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 8,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Second Bond Weld Peeling",
			"Vim300_Code": 1058,
			"Vision_Defect_Code": 9,
			"Label_Class": 8,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 3,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 10,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 11,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 12,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 13,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 14,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 15,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 16,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 17,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Second Bond Stub Bond Distance Error",
			"Vim300_Code": 1059,
			"Vision_Defect_Code": 18,
			"Label_Class": 9,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 3,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 19,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 20,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 21,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 22,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Confirm Later",
			"Vim300_Code": 1190,
			"Vision_Defect_Code": 255,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wedge",
			"Catagory_ID": 3,
			"Colour": [
				[0, 0, 0]
			]
		},
		{
			"Defect_Code": "Second Bond Normal",
			"Vim300_Code": 0,
			"Vision_Defect_Code": 0,
			"Label_Class": 0,
			"Is_Good": 0,
			"Label_Catagory": "bsob",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Second Bond Missing Weld",
			"Vim300_Code": 1050,
			"Vision_Defect_Code": 1,
			"Label_Class": 1,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Second Bond Broken Wire",
			"Vim300_Code": 1051,
			"Vision_Defect_Code": 2,
			"Label_Class": 2,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Second Bond Missing Weld",
			"Vim300_Code": 1050,
			"Vision_Defect_Code": 3,
			"Label_Class": 1,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 3,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Second Bond Weld ACC",
			"Vim300_Code": 1054,
			"Vision_Defect_Code": 4,
			"Label_Class": 4,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Second Bond Width Rejection",
			"Vim300_Code": 8888,
			"Vision_Defect_Code": 5,
			"Label_Class": 5,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Second Bond Length Rejection",
			"Vim300_Code": 8888,
			"Vision_Defect_Code": 6,
			"Label_Class": 6,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Second Bond Weld Clearance Error",
			"Vim300_Code": 1052,
			"Vision_Defect_Code": 7,
			"Label_Class": 7,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 8,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Second Bond Weld Peeling",
			"Vim300_Code": 1058,
			"Vision_Defect_Code": 9,
			"Label_Class": 8,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 10,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 11,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 12,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 13,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 14,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 15,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 16,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 17,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Second Bond Stub Bond Distance Error",
			"Vim300_Code": 1059,
			"Vision_Defect_Code": 18,
			"Label_Class": 9,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 2,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 19,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 20,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 21,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 22,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 255,
			"Colour": [
				[0, 128, 0]
			]
		},
		{
			"Defect_Code": "Confirm Later",
			"Vim300_Code": 1190,
			"Vision_Defect_Code": 255,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "bsob",
			"Catagory_ID": 2,
			"Colour": [
				[0, 0, 0]
			]
		},
		{
			"Defect_Code": "Wire Trace Normal",
			"Vim300_Code": 0,
			"Vision_Defect_Code": 0,
			"Label_Class": 0,
			"Is_Good": 0,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Wire Trace No Wire",
			"Vim300_Code": 1104,
			"Vision_Defect_Code": 1,
			"Label_Class": 1,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Wire Trace Wire Deviation",
			"Vim300_Code": 1105,
			"Vision_Defect_Code": 2,
			"Label_Class": 2,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Wire Trace Wire Too Close",
			"Vim300_Code": 1102,
			"Vision_Defect_Code": 3,
			"Label_Class": 3,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Wire Trace Broken Wire",
			"Vim300_Code": 1100,
			"Vision_Defect_Code": 4,
			"Label_Class": 4,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Wire Trace Snake Wire",
			"Vim300_Code": 1106,
			"Vision_Defect_Code": 5,
			"Label_Class": 5,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 6,
			"Label_Class": 6,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 7,
			"Label_Class": 7,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Wire Trace Short Wire",
			"Vim300_Code": 1103,
			"Vision_Defect_Code": 8,
			"Label_Class": 8,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Wire Trace Wire Sway",
			"Vim300_Code": 1101,
			"Vision_Defect_Code": 9,
			"Label_Class": 9,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Wire Trace Abnormal Wire Width",
			"Vim300_Code": 1107,
			"Vision_Defect_Code": 10,
			"Label_Class": 10,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Wire Trace Abnormal Wire Length",
			"Vim300_Code": 1108,
			"Vision_Defect_Code": 11,
			"Label_Class": 11,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 12,
			"Label_Class": 12,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Not Supported",
			"Vim300_Code": 9999,
			"Vision_Defect_Code": 13,
			"Label_Class": 13,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 1,
			"Colour": [
				[0, 0, 128]
			]
		},
		{
			"Defect_Code": "Confirm Later",
			"Vim300_Code": 1090,
			"Vision_Defect_Code": 255,
			"Label_Class": 255,
			"Is_Good": 1,
			"Label_Catagory": "wire",
			"Catagory_ID": 255,
			"Colour": [
				[0, 0, 0]
			]
		}
	]
}
