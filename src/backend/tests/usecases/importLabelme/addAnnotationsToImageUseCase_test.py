from usecase.importLabelme.addAnnotationsToImageUseCase import AddAnnotationsToImageUseCase
from ..utility.findHelper import Finder
from ..utility.objectMother import (
    Mother,
    MockAddCategoriesToDatasetUseCase
)
from ..utility.usecaseFixture import (
    mongo_connection_setup
)

class TestCase:

    def test_add_annotations_to_image(self, mongo_connection_setup):
        # Arrange
        category_data_list = self.get_category_data_list()
        annotation_data_list = self.get_annotation_data_list()
        image_id = Mother.create_image()
        category_id_map = self.create_categories(category_data_list, image_id)
        # Act
        usecase = AddAnnotationsToImageUseCase()
        annotation_id_list = usecase.execute(image_id, category_id_map, annotation_data_list)
        # Assert
        self.assert_annotation_equal_to(annotation_id_list, annotation_data_list)
        self.assert_num_of_annotations_in_image(image_id, annotation_id_list)
        # assert image_id, category_id of annotation list

    def get_annotation_data_list(self):
        return [{
            "image_id": 0, 
            "segmentation": [
                [
                    947.0, 
                    1127.0, 
                    943.0, 
                    1126.0, 
                    922.0, 
                    1151.0, 
                    922.0, 
                    1156.0, 
                    925.0, 
                    1155.0, 
                    945.0, 
                    1133.0
                ]
            ], 
            "metadata": {
                "class": "first defect",
                "Type": "rectangle"
            },
            "id": 0
        }, {
            "image_id": 0, 
            "segmentation": [
                [
                    947.0, 
                    1127.0, 
                    943.0, 
                    1126.0, 
                    922.0, 
                    1151.0, 
                    922.0, 
                    1156.0, 
                    925.0, 
                    1155.0, 
                    945.0, 
                    1133.0
                ]
            ], 
            "id": 1,
            "metadata": {
                "Type": "polygon"
            }
        }]

    def get_category_data_list(self):
        return [
            {
                "id": 0, 
                "name": "wire"
            }, 
        ]

    def create_categories(self, category_data_list, image_id):
        dataset_id = 0
        return MockAddCategoriesToDatasetUseCase().execute(category_data_list, dataset_id, image_id)

    def assert_annotation_equal_to(self, annotation_id_list, annotation_data_list):
        assert len(annotation_id_list) == len(annotation_data_list)
        for (index, annotation_id) in enumerate(annotation_id_list):
            annotation = Finder.find_annotation_by(annotation_id)
            print('annotation information')
            print('image id: ' + str(annotation.image_id))
            print('categories id: ' + str(annotation.category_id))
            assert annotation.segmentation == annotation_data_list[index]['segmentation']
            assert annotation.metadata == annotation_data_list[index]['metadata']
        
    def assert_num_of_annotations_in_image(self, image_id, annotation_id_list):
        image = Finder.find_image_by(image_id)
        assert image.annotated == True
        num_of_annotations = len(annotation_id_list)
        assert image.num_annotations == num_of_annotations
