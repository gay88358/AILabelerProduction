from database import (
    ImageModel,
    CategoryModel,
)

from .dataHolder import DataHolder
from .updateAnnotationsUsecsae import UpdateAnnotationsUsecase
from .updateAllImagesInTheDatasetUsecase import UpdateAllImagesInTheDatasetUsecase

class SaveAllAggregateDataUsecase:
    def __init__(self):
        self.data_hodler = None
        self.current_user = None

    def execute(self, data, current_user):
        self.data_hodler = DataHolder(data)
        self.current_user = current_user

        if self.image_is_not_exist():
            return {'success': False, 'message': 'Image does not exist'}, 400
        
        dataset_id = self.find_dataset_id()
        if self.user_can_not_access_dataset(dataset_id):
            return {'success': False, 'message': 'Could not find associated dataset'}

        self.update_dataset(self.find_dataset_in_the_user(dataset_id))

        self.update_user_preferences()

        self.update_all_category(data, current_user)

        num_annotations = UpdateAnnotationsUsecase().execute(data, current_user)

        UpdateAllImagesInTheDatasetUsecase().execute(num_annotations, self.data_hodler)
        return {"success": True}

    def find_dataset_id(self):
        image_model = ImageModel.objects(id=self.data_hodler.get_update_image_id()).first()
        return image_model.dataset_id

    def image_is_not_exist(self):
        image_id = self.data_hodler.get_update_image_id()
        return ImageModel.objects(id=image_id).first() is None

    def user_can_not_access_dataset(self, dataset_id):
        return self.find_dataset_in_the_user(dataset_id) is None

    def find_dataset_in_the_user(self, dataset_id):
        return self.current_user.find_dataset_by_id(dataset_id)

    def update_dataset(self, db_dataset):
        dataset_data = self.data_hodler.get_dataset_data()
        db_dataset.update(annotate_url=dataset_data.get('annotate_url', ''))

    def update_user_preferences(self):
        preference_to_update = self.data_hodler.get_user_preferences()
        self.current_user.change_preference(preference_to_update)
    # need to test
    def update_all_category(self, data, current_user):
        for category_data in data.get('categories', []):
            db_category = CategoryModel.find_by(category_data.get('id'))
            if db_category is None:
                continue
            self.update_category(db_category, category_data, current_user)

    def update_category(self, category, category_data, current_user):
        update_data = {'color': category_data.get('color')}
        if current_user.can_edit(category):
            update_data['keypoint_edges'] = category_data.get('keypoint_edges', [])
            update_data['keypoint_labels'] = category_data.get('keypoint_labels', [])
            update_data['keypoint_colors'] = category_data.get('keypoint_colors', [])
        category.update(**update_data)