
from usecase.importLabelme.labelmeChecker import LabelChecker

class TestCase:

    def test_check_labelme_str(self):
        labelme_str = '{"Labels": []}'
        result = LabelChecker.check_string(labelme_str)
        assert  result.is_success() == True

    def test_check_empty_labelme_json(self):
        labelme_json = self.get_empty_labelme_json()

        result = LabelChecker.check(labelme_json)

        assert result.is_success() == True
    
    def get_empty_labelme_json(self):
        return {
            "Labels": []
        }

    def test_check_normal_labelme_json(self):
        labelme_json = self.get_normal_labelme_json()

        result = LabelChecker.check(labelme_json)

        assert result.is_success() == True

    def get_normal_labelme_json(self):
        return {
            'Labels': [
                {
                    "Label": "wire",
                    "Shapes": [
                        {
                            'Type': "",
                            'points': [],
                            'Score': 0,
                            'Attributes': {}
                        }
                    ]
                }
            ]
        }

    def test_check_invalid_labelme_json(self):
        labelme_json = self.get_invalid_labelme_json()
        result = LabelChecker.check(labelme_json)

        assert result.is_success() == False
        assert LabelChecker.INVALID_TYPE in result.error_messages
        assert LabelChecker.INVALID_POINTS in result.error_messages
        assert LabelChecker.INVALID_ATTRIBUTES in result.error_messages
        
    def get_invalid_labelme_json(self):
        return {
            'Labels': [
                {
                    "Label": "wire",
                    "Shapes": [
                        {
                            'Type': "",
                            'points': [],
                            'Score': 0,
                            'Attributes': {}
                        },
                        {

                        }
                    ]
                }
            ]
        }