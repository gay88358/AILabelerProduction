import pytest
from usecase.util.jsonHelper import JsonHelper
 
def get_labelme_json_path():
    import os
    base_dir = os.path.dirname(__file__)
    return base_dir + '/testData/machine_labelme.json'

def restore_document(json_file_path, original_document):
    JsonHelper.write_json(json_file_path, original_document)

@pytest.fixture()
def json_file_path():
    json_file_path = get_labelme_json_path()
    original_document = JsonHelper.load_json_document(json_file_path)
    yield json_file_path
    restore_document(json_file_path, original_document)
    

class TestCase:

    def test_replace_json_document(self, json_file_path):
        # json_file_path = self.get_labelme_json_path()
        document_want_to_replace = {
            "Labels": []
        }
        JsonHelper.replace_document(json_file_path, document_want_to_replace)
        result = JsonHelper.load_json_document(json_file_path)
        assert document_want_to_replace['Labels'] == result['Labels']
    