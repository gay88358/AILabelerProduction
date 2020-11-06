from database import UserModel
from ..usecases.utility.objectMother import Mother

from ..usecases.utility.usecaseFixture import (
    mongo_connection_setup
)

from ..usecases.utility.findHelper import (
    Finder
)

class TestCase:
    def test_add_new_dataset_name_list_to_user(self, mongo_connection_setup):
        dataset_name_list = self.get_dataset_name_list()

        user = self.create_user_with_shared_folder(dataset_name_list)

        assert user.dataset_name_list == dataset_name_list

    def test_add_additional_dataset_name_list_to_user(self, mongo_connection_setup):
        dataset_name_list_to_add = self.get_dataset_name_list()
        user = self.create_user_with_shared_folder(dataset_name_list_to_add)
        original_dataset_name_list = user.dataset_name_list
        # Act
        self.add_shared_folder_to(user, dataset_name_list_to_add)
        # Assert
        assert user.dataset_name_list == original_dataset_name_list + dataset_name_list_to_add 
    
    def create_user_with_shared_folder(self, dataset_name_list):
        user_id = Mother.create_user("Zi-Xuan", "123")
        user = Finder.find_user_by_id(user_id)
        self.add_shared_folder_to(user, dataset_name_list)
        return user
    
    def add_shared_folder_to(self, user, dataset_name_list):
        user.add_shared_folder(self.get_root(), dataset_name_list, self.get_mount_directory())

    def get_dataset_name_list(self):
        return ["ZZZ", "XXX", "YYY"]

    def get_root(self):
        return "fake root"
    
    def get_mount_directory(self):
        return "fake mount directory"