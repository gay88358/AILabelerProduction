


from usecase.saveAggregateData.updateAllImagesInTheDatasetUsecase import UpdateAllImagesInTheDatasetUsecase

from ..utility.usecaseFixture import (
    mongo_connection_setup
)

from ..utility.findHelper import (
    Finder
)

from ..utility.objectMother import (
    FakeDataset, Mother, FakeCurrentUser
)

class MockUpdateAllImagesInTheDatasetUsecase(UpdateAllImagesInTheDatasetUsecase):
    def generate_thumbnail(self, image_model):
        pass



class TestCase:

    def test_update_all_image_in_the_dataset(self, mongo_connection_setup):
        # Arrange
        self.create_images()
        image_id = self.get_image_id()
        num_annotations = 3
        image_data = self.get_image_data()
        usecase = MockUpdateAllImagesInTheDatasetUsecase()
        # Act
        usecase.update_all_images_in_the_dataset(image_id, num_annotations, image_data)
        # Assert
        self.assert_all_images_in_the_dataset_equals_to(image_data, num_annotations)

    def assert_all_images_in_the_dataset_equals_to(self, image_data, num_annotations):
        for image in Finder.find_all_images():
            self.assert_image_equals_to(image_data, image.id, num_annotations)

    def create_images(self):
        Mother.create_image_by("img1")
        Mother.create_image_by("img2")
        Mother.create_image_by("img3")

    def get_image_id(self):
        return Finder.find_all_images()[0].id

    def test_update_image_with_image_data(self, mongo_connection_setup):
        # Arrange
        image_id = Mother.create_image()
        image_data = self.get_image_data() # data structure coming from http request
        num_annotations = 3
        image_to_update = Finder.find_image_by(image_id)
        usecase = MockUpdateAllImagesInTheDatasetUsecase()
        # Act
        usecase.update_image(num_annotations, image_data, image_to_update)
        # Assert
        self.assert_image_equals_to(image_data, image_id, num_annotations)
    
    def assert_image_equals_to(self, image_data, image_id, num_annotations):
        image = Finder.find_image_by(image_id)
        assert image.metadata == image_data.get('metadata', {})
        assert image.annotated == (num_annotations > 0)
        assert image.category_ids == image_data.get('category_ids', {})
        assert image.regenerate_thumbnail == True
        assert image.num_annotations == num_annotations

    def get_image_data(self):
        return {
            "metadata": {
                "test": "gogd"
            },
            "category_ids": [1, 2, 3],
        }
 