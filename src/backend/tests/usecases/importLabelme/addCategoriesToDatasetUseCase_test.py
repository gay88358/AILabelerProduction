from ..utility.findHelper import Finder
from ..utility.objectMother import (
    Mother,
    MockAddCategoriesToDatasetUseCase,
    FakeDataset
)

from ..utility.usecaseFixture import (
    mongo_connection_setup
)

class TestCase:
    def test_add_categories_to_dataset(self, mongo_connection_setup):
        # Arrange
        category_data_list = self.get_category_data_list()
        dataset_id = 1
        image_id = Mother.create_image()
        old_image_category_id_list = self.set_image_category_id_list(image_id)
        # mock usecase setup
        fake_data_set = FakeDataset()
        usecase = MockAddCategoriesToDatasetUseCase()
        usecase.set_fake_dataset_to_return(fake_data_set)
        # Act
        category_id_map = usecase.execute(category_data_list, dataset_id, image_id)
        # Assert
        self.assert_category_equals_to(category_data_list, category_id_map)
        self.assert_image_contains_categories_id(image_id, category_id_map, old_image_category_id_list)
        fake_data_set.categories_should_be(self.fetch_category_id_list(category_id_map))

    def get_category_data_list(self):
        return [
            {
                "id": 0, 
                "name": "wire"
            }, 
            {
                "id": 1, 
                "name": "bond_rec"
            }, 
        ]

    def set_image_category_id_list(self, image_id):
        old_image_category_id_list = [0]
        image = Finder.find_image_by(image_id)
        image.update(set__category_ids = old_image_category_id_list)
        return old_image_category_id_list

    def assert_category_equals_to(self, category_data_list, category_id_map):
        assert len(category_data_list) == len(category_id_map)

        for (category_data_id, category_id) in category_id_map.items():
            category = Finder.find_category_by(category_id)
            category_data = self.find_category_data_by(category_data_id, category_data_list)
            assert category.name == category_data['name']
    
    def find_category_data_by(self, category_data_id, category_data_list):
        return list(filter(lambda c: c['id'] == category_data_id, category_data_list))[0]
    
    def assert_image_contains_categories_id(self, image_id, category_id_map, old_image_category_id_list):
        image = Finder.find_image_by(image_id)
        expected_category_id_list = sorted(image.category_ids)

        new_added_category_id_list = self.fetch_category_id_list(category_id_map)
        actual_category_id_list = sorted(new_added_category_id_list + old_image_category_id_list)
        
        assert actual_category_id_list == expected_category_id_list

    def fetch_category_id_list(self, category_id_map):
        return list(category_id_map.values())