



from database.sharedFolder import SharedFolder


class TestCase:
    def create_shared_folder(self):
        root = "path root"
        names = ["dataset1", "dataset2", "dataset3"]
        mount_root = "mount root"
        return SharedFolder(root, names, mount_root)

    def test_get_mount_directory_by_invalid_dataset_name(self):
        # Act
        folder = self.create_shared_folder()
        # Assert  
        try:      
            folder.get_mount_directory("dataset3123")
            self.failed()
        except ValueError: 
            self.passed()
    
    def passed(self):
        assert 1 == 1

    def failed(self):
        assert 1 == 2

    def test_get_mount_directory_by_dataset_name(self):
        # Arrange
        root = "path root"
        names = ["dataset1", "dataset2", "dataset3"]
        mount_root = "mount root"
        # Act
        folder = SharedFolder(root, names, mount_root)
        # Assert        
        assert folder.get_mount_directory("dataset1") == "mount root/dataset1"
        assert folder.get_mount_directory("dataset2") == "mount root/dataset2"
        assert folder.get_mount_directory("dataset3") == "mount root/dataset3"

