from usecase.importLabelme.importAnnotationsToAllImagesUsecase import ImportAnnotationsToImageUsecase
from usecase.importLabelme.importAnnotationsToAllImagesUsecase import ImportAnnotationsToAllImagesUsecase
from usecase.util.jsonHelper import JsonHelper

from ..utility.findHelper import Finder
from ..utility.objectMother import (
    Mother,
    MockAddCategoriesToDatasetUseCase,
    FakeDataset
)
import functools 
import operator 
from ..utility.usecaseFixture import (
    mongo_connection_setup
)

class TestCase:
    def test_import_annotations_to_all_images(self, mongo_connection_setup):
        # Arrange
        dataset_id = 1
        self.create_images()
        labelme_json_string = self.load_labelme_json_string()
        fakeDataset = FakeDataset()
        mock_add_category_to_dataset_usecase = MockAddCategoriesToDatasetUseCase()
        mock_add_category_to_dataset_usecase.set_fake_dataset_to_return(fakeDataset)
        usecase = ImportAnnotationsToAllImagesUsecase.create_by(mock_add_category_to_dataset_usecase)
        # Act
        result = usecase.execute(dataset_id, labelme_json_string)
        # Assert
        assert result.is_success()
        self.assert_import_annotations_to_all_images(dataset_id)
        fakeDataset.categories_size_should_be(5)

    def create_import_annotation_to_image(self, fakeDataset):
        mock_add_category_to_dataset_usecase = MockAddCategoriesToDatasetUseCase()
        mock_add_category_to_dataset_usecase.set_fake_dataset_to_return(fakeDataset)
        return MockImportAnnotationToImageUsecase(mock_add_category_to_dataset_usecase)


    def create_images(self):
        Mother.create_image_by('img1')
        Mother.create_image_by('img2')
        Mother.create_image_by('img3')

    def assert_import_annotations_to_all_images(self, dataset_id):
        images = Mother.find_images_by_dataset_id(dataset_id)
        assert len(images) == 3
        for image in images:
            image_id = image.id
            self.assert_image_contains_correct_num_annotations(image_id)
            self.assert_category_num()
            self.assert_annotation_num(image_id)
            self.assert_annotation_is_distributed_across_category_correctly()

    def load_labelme_json_string(self):
        import os
        base_dir = os.path.dirname(__file__)
        return JsonHelper.load_json_string(base_dir + '/usecaseTestData/machine_labelme.json')

    def assert_image_contains_correct_num_annotations(self, image_id):
        image = Finder.find_image_by(image_id)
        assert image.num_annotations == 37

    def assert_category_num(self):
        categories = Finder.find_all_categories()
        assert len(categories) == 5

    def assert_annotation_num(self, image_id):
        annotations = Finder.find_annotations_by(image_id)
        assert len(annotations) == 37

    def assert_annotation_is_distributed_across_category_correctly(self):
        categories = Finder.find_all_categories()

        num_annotations_for_each_category = list(map(
            lambda c: len(Finder.find_annotations_by_category_id(c.id)),
            categories
        ))

        num_annotations_for_all_category = functools.reduce(
            operator.add,
            num_annotations_for_each_category
        )
        assert num_annotations_for_all_category == 111
