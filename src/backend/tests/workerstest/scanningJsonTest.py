import os

from workers.tasks.jsonFileFinder import JsonFileFinder

from usecase.util.jsonHelper import JsonHelper
 
class TestCase:
    


    def test_adsf(self):
        # Arrange
        self.create_json_file()
        finder = JsonFileFinder()
        # Act
        size = finder.find_json_in_the("/Users/koushiken/Desktop/ATWEX/stripID_2/logcaseR2")
        # Assert
        assert 2 == 1

    # def test_scanning_json_file(self):
    #     # Arrange
    #     self.create_json_file()
    #     finder = JsonFileFinder()
    #     # Act
    #     json_string = finder.find_json_in_the(os.path.dirname(__file__))
    #     # Assert
    #     assert json_string == '{"test": "123"}'
    #     self.delete_json_file()

    # def test_scanning_json_file_not_found(self):
    #     # Arrange
    #     finder = JsonFileFinder()
    #     # Act
    #     json_string = finder.find_json_in_the(os.path.dirname(__file__))
    #     # Assert
    #     assert json_string == ""

    def delete_json_file(self):
        os.remove(self.json_file_path())

    def create_json_file(self):
        JsonHelper.write_json(self.json_file_path(), {"test": "123"})

    def json_file_path(self):        
        import os
        base_dir = os.path.dirname(__file__)
        directory = base_dir + '/test.json'
        return directory