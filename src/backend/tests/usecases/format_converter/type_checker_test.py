import pytest

from usecase.exportLabelme.coco2labelme.typeChecker.typeChecker import *

class TestCase:

    def test_get_type_with_the_document_contains_metadata(self):
        DUMMY_INDEX = 0
        coco_document = self.create_coco_document()
        checker = NormalTypeChecker()

        assert True == checker.is_given_type(DUMMY_INDEX, coco_document)
        assert 'Circle' == checker.get_type()

    def create_coco_document(self):
        result = {}
        result['metadata'] = {}
        result['metadata']['Type'] = 'Circle'
        return result   
        
    def test_get_type_with_the_document_is_not_contains_metadata(self):
        DUMMY_INDEX = 0
        checker = NormalTypeChecker()

        assert False == checker.is_given_type(DUMMY_INDEX, self.create_document_without_metadata())

    def create_document_without_metadata(self):
        result = {}
        return result
