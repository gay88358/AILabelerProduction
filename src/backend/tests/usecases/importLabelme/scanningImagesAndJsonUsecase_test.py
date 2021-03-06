from usecase.importLabelme.scanningImagesAndJsonUsecase import (
    ImageRepository,
)

from ..utility.usecaseFixture import (
    mongo_connection_setup
)

from ..utility.findHelper import (
    Finder
)

from ..utility.objectMother import (
    FakeDataset
)

class MockImageCreator(ImageRepository):
    def __init__(self, dataset):
        self.dataset = dataset
    

    def create_thumbnail_for_all_images(self):
        pass

    def find_dataset_by(self, dataset_id):
        return self.dataset

    def set_dataset_by(self, dataset_id):
        pass

class TestCase:

    def test_sanning_image_and_json(self, mongo_connection_setup):
        # Arrange
        dataset_id = 0
        directory = self.get_directory()
        fakeDataset = FakeDataset()
        fakeDataset.set_directory(directory)
        fakeDataset.set_id(dataset_id)
        scanner = MockImageCreator(fakeDataset)
        # Act
        scanner.create_images_from(dataset_id)
        # Assert
        images = Finder.find_all_images()
        assert len(images) == 3
    
    def get_directory(self):
        import os
        base_dir = os.path.dirname(__file__)
        return base_dir + "/scanningData"
        