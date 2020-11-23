

from usecase.importLabelme.createNewDatasetUsecase import CreateNewDatasetUsecase
from ..utility.objectMother import FakeDataset



class DatasetFactory:


    def __init__(self, dataset = None):
        self.dataset = dataset

    def create_dataset(self):
        if self.dataset == None:
            raise ValueError('')
        return self.dataset

class MockCreateNewDatasetUsecase(CreateNewDatasetUsecase):
    def __init__(self, dataset_factory):
        self.dataset_factory = dataset_factory
    
    def create_dataset(self, dataset_name):
        return self.dataset_factory.create_dataset()
    

class TestCase:

    def test_create_all_dataset_with_duplicate_name(self):
        # Arrange
        dataset_name_list = ["first dataset", "first dataset"]
        usecase = MockCreateNewDatasetUsecase(DatasetFactory())
        # Act
        result = usecase.create_all_dataset(dataset_name_list)
        # Assert
        assert result.is_failure()
        assert result.error_messages == ['Dataset name is duplicate: first dataset']
        
    def test_create_all_dataset_with_result(self):
        # Arrange
        dataset_name_list = ["first dataset", "second dataset"]
        fakeDataset = FakeDataset()
        usecase = MockCreateNewDatasetUsecase(DatasetFactory(fakeDataset))
        # Act
        result = usecase.create_all_dataset(dataset_name_list)
        assert result.value == [1, 1]
        assert result.is_success()
        self.assert_dataset_length(2, result)
        
    def assert_dataset_length(self, expected_length, result):
        assert len(result.value) == expected_length
