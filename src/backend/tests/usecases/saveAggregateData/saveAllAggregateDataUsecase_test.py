


from usecase.saveAggregateData.saveAllAggregateDataUsecase import (
    SaveAllAggregateDataUsecase,
    UpdateAnnotationsUsecase
)

from ..utility.usecaseFixture import (
    mongo_connection_setup
)

from ..utility.findHelper import (
    Finder
)

from ..utility.objectMother import (
    FakeDataset, Mother, FakeCurrentUser
)


class MockAUpdateAnnotationsUsecase(UpdateAnnotationsUsecase):
    def generate_coco_format_for_segment_data(self, width, height, paperjs_object):
        segmentation = [[1, 2, 3, 4]]
        area = 20
        bbox = [1, 2, 3, 4]
        return segmentation, area, bbox

class MockSaveAllAggregateDataUsecase(SaveAllAggregateDataUsecase):
    # seam point
    def generate_thumbnail(self, image_model):
        pass



class TestCase:
    
    def test_update_category_with_category_data(self, mongo_connection_setup):
        # Arrange
        category_id = Mother.create_category()
        category_data = {
            "color": "red",
            "keypoint_edges": [1, 2, 3, 4],
            "keypoint_labels": [1, 2, 3, 54],
            "keypoint_colors": [1, 2, 3, 4]
        }
        usecase = MockSaveAllAggregateDataUsecase()
        fake_current_user = FakeCurrentUser()
        # Act
        usecase.update_category(
            Finder.find_category_by(category_id), 
            category_data, 
            fake_current_user
        )
        # Assert
        self.assert_category_equals_to(category_data, category_id)
    
    def assert_category_equals_to(self, category_data, category_id):
        category = Finder.find_category_by(category_id)
        category.color = category_data["color"]
        category.keypoint_edges = category_data["keypoint_edges"]
        category.keypoint_labels = category_data["keypoint_labels"]
        category.keypoint_colors = category_data["keypoint_colors"]