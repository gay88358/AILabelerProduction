from ..utility.findHelper import Finder
from ..utility.objectMother import (
    Mother,
    MockAddCategoriesToDatasetUseCase,
    FakeDataset
)

from ..utility.usecaseFixture import (
    mongo_connection_setup
)

from usecase.importLabelme.addSharedFolderUsecase import AddSharedFolderUsecase

class TestCase:
    def test_adda_shared_folder_to_user(self, mongo_connection_setup):
        # Arrange
        user = self.create_user()
        stripID = "stripID_1"
        dataset_name_list = ['logcase1', 'logcase2', 'logcase3']
        mount_directory = "/worksapce/sharedFolder/ATWEX"
        usecase = AddSharedFolderUsecase()
        # Act
        usecase.execute(user, stripID, dataset_name_list, mount_directory)
        # Assert
        shared_folder = self.get_shared_folder(user)
        assert "/worksapce/sharedFolder/ATWEX/stripID_1/logcase1" == shared_folder.get_mount_directory("stripID_1/logcase1")
        assert "/worksapce/sharedFolder/ATWEX/stripID_1/logcase2" == shared_folder.get_mount_directory("stripID_1/logcase2")
        assert "/worksapce/sharedFolder/ATWEX/stripID_1/logcase3" == shared_folder.get_mount_directory("stripID_1/logcase3")

    def get_shared_folder(self, user):
        return Finder.find_user_by_id(user.id).get_shared_folder()

    def create_user(self):
        user_id = Mother.create_user("Zi-Xuan", "asm")
        return Finder.find_user_by_id(user_id)
