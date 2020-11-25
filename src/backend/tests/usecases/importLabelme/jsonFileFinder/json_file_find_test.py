import pytest

from usecase.importLabelme.jsonFileFinder import JsonFileFinder
from usecase.importLabelme.filePathFinder import FilePathFinder
from usecase.util.jsonHelper import JsonHelper

class RelativePathFormater:
    @staticmethod
    def to_absolute_path(relative_path):
        import os
        base_dir = os.path.dirname(__file__)
        directory = base_dir + relative_path
        return directory

@pytest.fixture()
def json_file_directory():
    directory = RelativePathFormater.to_absolute_path ('/testData')
    FilePathFinder.delete_all_contents_in(directory)
    return directory

class TestCase:
    def test_directory_is_not_include_label_json(self, json_file_directory):
        # Arrange
        finder = JsonFileFinder()
        # Act
        result = finder.find_label_json_in_the(json_file_directory)
        # Assert
        assert result.is_failure
        assert "must contains Label.json" in result.error_messages[0]
    
    def test_directory_is_include_label_json(self, json_file_directory):
        # Arrange
        fake_label_document = {}
        self.prepare_label_json(json_file_directory, fake_label_document)
        finder = JsonFileFinder()
        # Act
        result = finder.find_label_json_in_the(json_file_directory)
        # Assert
        assert result.is_success()

    def prepare_label_json(self, json_file_directory, label_document):
        JsonHelper.write_json(
            self.label_json_directory(json_file_directory),
            label_document
        )

    def test_directory_is_include_wrong_format_label_json(self, json_file_directory):
        # Arrange
        invalid_label_str = "{"
        self.prepare_label_json_str(json_file_directory, invalid_label_str)
        finder = JsonFileFinder()
        # Act
        result = finder.find_label_json_in_the(json_file_directory)
        # Assert
        assert result.is_failure()
        assert "please check the format of json file" in result.error_messages[0]

    def prepare_label_json_str(self, json_file_directory, label_document_str):
        JsonHelper.write_json_str(
            self.label_json_directory(json_file_directory),
            label_document_str
        )

    def label_json_directory(self, json_file_directory):
        return "{}/Label.json".format(json_file_directory)