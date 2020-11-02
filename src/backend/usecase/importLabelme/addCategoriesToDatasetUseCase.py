from database import CategoryModel, ImageModel, DatasetModel

class AddCategoriesToDatasetUseCase:
    def __init__(self):
        pass

    def execute(self, categories_date, dataset_id, image_id):
        category_id_map = self.create_all_categories(categories_date)
        self.update_category_id_of_image(category_id_map, image_id)
        self.update_category_id_of_dataset(category_id_map, dataset_id)
        return category_id_map
    
    def create_all_categories(self, categories_date):
        result = {}
        for c in categories_date:
            category_id = self.create_category(c)
            category_data_id = c['id']
            result[category_data_id] = category_id
        return result

    def create_category(self, category_data):
        
        exist_category = CategoryModel.find_by_name(category_data['name'])
        if exist_category is not None:
            return exist_category.id
        

        category = CategoryModel(
                name=category_data['name'],
                supercategory="supercategory",
                color="color",
                metadata={},
                keypoint_edges=[],
                keypoint_labels=[],
                keypoint_colors=[],
        )
        category.save()
        return category.id

    def update_category_id_of_image(self, category_id_map, image_id):
        category_id_list_to_add = self.fetch_category_ids(category_id_map)

        image = ImageModel.find_by(image_id)
        image.add_category_id_list(category_id_list_to_add)

    def update_category_id_of_dataset(self, category_id_map, dataset_id):
        category_id_list = self.fetch_category_ids(category_id_map)
        # untest: potential bug point
        dataset = self.find_dataset_by(dataset_id)
        dataset.update_categories(category_id_list)
    
    # seam point: override by mock object to isolate dependency and can't inline
    def find_dataset_by(self, dataset_id):
        return DatasetModel.find_by(dataset_id)

    def fetch_category_ids(self, category_id_map):
        return list(category_id_map.values())