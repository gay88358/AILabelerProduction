import os


from usecase.importLabelme.mountDirectory import format_mount_directory

class TestCase:
    def test_format_invalid_mount_directory(self):
        mount_directory = "sdf"
        dataset_name = "sdf"
        result = format_mount_directory(mount_directory, dataset_name)
        assert result.is_success() == False
    
    def test_format_mount_directory(self):
        base_dir = os.path.dirname(__file__)
        mount_directory = base_dir
        dataset_name = "fakeDatasetDirectory"
        result = format_mount_directory(mount_directory, dataset_name)
        assert result.is_success() == True
    