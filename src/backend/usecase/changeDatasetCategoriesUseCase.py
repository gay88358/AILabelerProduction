from database import (
    DatasetModel,
    CategoryModel
)

class ChangeDatasetCategoriesUseCase:
    def execute(self, dataset_id, categories):
        dataset = DatasetModel.find_by(dataset_id)
        category_id_list = CategoryModel.bulk_create(categories)
        # dataset.update(set__categories=category_id_list)
        dataset.update_categories(category_id_list)
        