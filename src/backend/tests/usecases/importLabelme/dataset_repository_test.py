from ..utility.findHelper import Finder
from ..utility.objectMother import (
    Mother,
    FakeDataset,
    MockImage
)

from ..utility.usecaseFixture import (
    mongo_connection_setup
)

from usecase.importLabelme.datasetRepository import DatasetRepository


class MockDatasetRepository(DatasetRepository):

    def __init__(self):
        self.dataset = None
        self.is_delete_directory_called = False

    def find_images_in(self, dataset):
        images = MockImage.find_images_by_dataset_id(dataset.id)
        return images

    def delete_whole_directory(self, dataset):
        self.is_delete_directory_called = True

    def find_datasets_by_stripID(self, stripId):
        if self.dataset == None:
            return None
        return [self.dataset]

    def withFakeDataset(self, dataset):
        self.dataset = dataset

    def should_delete_dataset_directory(self):
        assert self.is_delete_directory_called == True

class TestCase:

    def test_remove_dataset_with_invalid_stripID(self, mongo_connection_setup):
        # Arrange
        invalid_stripID = "invalid"
        repository = MockDatasetRepository()
        # Act
        result = repository.delete_by_stripId(invalid_stripID)
        # Assert
        assert result.is_success() == False

    def test_remove_dataset(self, mongo_connection_setup):
        # Arrange
        dataset_id = 1
        image_id = Mother.create_image_by("123123", dataset_id)
        annotation_id = Mother.create_annotation(image_id)
        dataset = self.create_fake_dataset(dataset_id)
        repository = MockDatasetRepository()
        repository.withFakeDataset(dataset)
        # Act
        result = repository.delete(dataset)
        # Assert
        self.assert_all_image_is_deleted(image_id)
        self.assert_all_annotation_is_deleted(annotation_id)
        repository.should_delete_dataset_directory()

    def create_fake_dataset(self, dataset_id):
        return FakeDataset(dataset_id)

    def assert_all_image_is_deleted(self, image_id):
        try:
            image = MockImage.objects.get(id=image_id)
            # fail
            assert 1 == 2
        except:
            pass
        
    
    def assert_all_annotation_is_deleted(self, annotation_id):
        annotation = Finder.find_annotation_by(annotation_id)
        assert annotation is None

    # def assert_all_category_is_deleted(self, dataset):
    #     category = FInder.find_category_by()

    # def assert_dataset_folder_is_deleted(self, dataset):
    #     pass

