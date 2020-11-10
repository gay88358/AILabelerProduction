from database import UserModel
from ..usecases.utility.objectMother import Mother

from ..usecases.utility.usecaseFixture import (
    mongo_connection_setup
)

from ..usecases.utility.findHelper import (
    Finder
)

class TestCase:

    def test_get_dataset_name_list_with_invalid_stripId(self, mongo_connection_setup):
        stripID = "stripID_1"
        user = self.create_user()
        try:
            user.get_dataset_name_list_with(stripID)
            assert  1 == 2
            self.fail()
        except ValueError as e:
            err_msg = str(e)
            assert err_msg == "Given stripID: stripID_1 is invalid"

    def fail(self):
        assert 1 == 2
    
    def success(self):
        pass

    def test_add_set_of_dataset_name_with_different_strip_id(self, mongo_connection_setup):
        # Arrange
        mount_directory = "/mount_directory"
        
        stripID_1 = "stripID_1"
        dataset_name_list_1 = ["1"]

        stripID_2 = "stripID_2"
        dataset_name_list_2 = ["2"]
        user = self.create_user()
        # Act
        user.add_strip_folder(stripID_1, dataset_name_list_1, mount_directory)
        user.add_strip_folder(stripID_2, dataset_name_list_2, mount_directory)
        # Assert
        assert user.get_dataset_name_list_with(stripID_1) == dataset_name_list_1
        assert user.get_dataset_name_list_with(stripID_2) == dataset_name_list_2

    def create_user(self):
        user_id = Mother.create_user("Zi-Xuan", "123")
        return Finder.find_user_by_id(user_id)

    def test_add_strip_id_with_dataset_name_list(self, mongo_connection_setup):
        # Arrange
        mount_directory = self.get_mount_directory()
        stripID = "stripID_1"
        dataset_name_list = self.get_dataset_name_list()
        user = self.create_user()
        # Act
        user.add_strip_folder(stripID, dataset_name_list, mount_directory)
        # Assert
        shared_folder = user.get_shared_folder_with(stripID)   
        assert user.get_dataset_name_list_with(stripID) == dataset_name_list 
        assert shared_folder.contains(dataset_name_list)
    
    def test_add_strip_id_with_dataset_name_list_should_contain_last_dataset_name(self, mongo_connection_setup):
        # Arrange
        mount_directory = self.get_mount_directory()
        stripID = "stripID_1"
        first_dataset_name_list = ["1"]
        second_dataset_name_list = self.get_dataset_name_list()
        user = self.create_user()
        # Act
        user.add_strip_folder(stripID, first_dataset_name_list, mount_directory)
        user.add_strip_folder(stripID, second_dataset_name_list, mount_directory)
        # Assert
        shared_folder = user.get_shared_folder_with(stripID) 
        assert not shared_folder.contains(first_dataset_name_list)  
        assert user.get_dataset_name_list_with(stripID) == second_dataset_name_list 
        assert shared_folder.contains(second_dataset_name_list)

    def get_dataset_name_list(self):
        return ["ZZZ", "XXX", "YYY"]

    
    def get_mount_directory(self):
        return "fake mount directory"