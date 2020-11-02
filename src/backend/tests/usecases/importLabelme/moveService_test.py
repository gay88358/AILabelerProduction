import pytest

from usecase.importLabelme.filePathFinder import FilePathFinder
from usecase.importLabelme.moveService import MoveService
from ..utility.objectMother import (
    FakeDataset
)

class MockImageRepository:
    def __init__(self):
        pass

    def delete_image_in_the(self, dataset):
        pass

class RelativePathFormater:
    @staticmethod
    def to_absolute_path(relative_path):
        import os
        base_dir = os.path.dirname(__file__)
        directory = base_dir + relative_path
        return directory

@pytest.fixture()
def dataset_directory():
    directory = RelativePathFormater.to_absolute_path ('/fakeDatasetDirectory')
    FilePathFinder.delete_all_contents_in(directory)
    return directory

class TestCase:
    def test_move_content_of_source_to_dataset(self, dataset_directory):
        dataset = self.create_dataset(dataset_directory)
        image_repository = MockImageRepository()
        service = MoveService(image_repository)
        # Act
        service.move_content_from_source_to_dataset(dataset, self.get_dataset_source_folder_path())
        # Assert        
        self.assert_dataset_directory_contains_moved_content(dataset)

    def create_dataset(self, directory):
        dataset = FakeDataset()
        dataset.set_directory(directory)
        return dataset

    def get_dataset_source_folder_path(self):
        return RelativePathFormater.to_absolute_path ('/usecaseTestData/')

    def assert_dataset_directory_contains_moved_content(self, dataset):
        paths = FilePathFinder.find_file_path_in(dataset.directory)   
        assert len(paths) == 1