


from usecase.datasets.findPaginationDatasetUsecase import FindPaginationDatasetUsecase

from ..utility.usecaseFixture import (
    mongo_connection_setup
)

from ..utility.findHelper import (
    Finder
)

from ..utility.objectMother import (
    FakeDataset, Mother, FakeCurrentUser
)


class MockPaginationDatasetUsecase(FindPaginationDatasetUsecase):
    def __init__(self):
        pass
    
    def find_datasets_by(self, dataset_folders):
        return [FakeDataset(1), FakeDataset(2)]

class TestCase:

    def test_find_pagination_dataset(self, mongo_connection_setup):
        # Arrange dataset_id = 1
        dataset1_id = 1
        image1_id = Mother.create_image_by("img1", dataset1_id)
        dataset2_id = 2
        image2_id = Mother.create_image_by("img2", dataset2_id)
        usecase = MockPaginationDatasetUsecase()
        stripID = "stripID_1"
        # Act
        result = usecase.execute(self.get_limit(), self.get_page(), stripID, FakeCurrentUser())
        # Assert
        self.assert_dataset_json(result, image1_id, image2_id)

    def get_limit(self):
        return 52
    
    def get_page(self):
        return 1

    def assert_dataset_json(self, result, image1_id, image2_id):
        assert result == {'pagination': {'start': 0, 'end': 2, 'pages': 1, 'page': 1, 'total': 2, 'showing': 2}, 'datasets': [{'id': 1, 'numberImages': 1, 'numberAnnotated': 0, 'permissions': 'permission1', 'first_image_id': image1_id}, {'id': 2, 'numberImages': 1, 'numberAnnotated': 0, 'permissions': 'permission1', 'first_image_id': image2_id}]}

    def assert_datasets_equals(self, datasets, expected_datasets):
        assert len(datasets) == len(expected_datasets)
 
        
    