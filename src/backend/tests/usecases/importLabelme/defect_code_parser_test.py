from usecase.importLabelme.loadDefectCode.defectCodeParser import DefectCodeParser

class TestCase:
    def test_parse_label_map_json_file(self):
        # Arrange
        label_map_document = self.create_label_map_document()
        parser = DefectCodeParser(label_map_document)
        # Act
        result = parser.to_defect_code_catalog()
        # Assert
        assert result['defectcode_catalog'][0] == {'category_name': 'ball', 'category_id': 0, 'defect_code_list': [{'Defect_Code': 'First Bond Normal', 'Vim300_Code': 0}, {'Defect_Code': 'First Bond Missing Bond', 'Vim300_Code': 1004}]}
        assert result['defectcode_catalog'][1] == {'category_name': 'wedge', 'category_id': 0, 'defect_code_list': [{'Defect_Code': 'Second Bond Normal', 'Vim300_Code': 0}, {'Defect_Code': 'Second Bond Missing Weld', 'Vim300_Code': 1050}]}
        assert result['defectcode_catalog'][2] == {'category_name': 'bsob', 'category_id': 0, 'defect_code_list': [{'Defect_Code': 'Second Bond Normal', 'Vim300_Code': 0}, {'Defect_Code': 'Second Bond Missing Weld', 'Vim300_Code': 1050}]}
        assert result['defectcode_catalog'][3] == {'category_name': 'wire', 'category_id': 0, 'defect_code_list': [{'Defect_Code': 'Wire Trace Normal', 'Vim300_Code': 0}, {'Defect_Code': 'Wire Trace No Wire', 'Vim300_Code': 1104}]}
    
    def create_label_map_document(self):
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
                
            ]
        }
