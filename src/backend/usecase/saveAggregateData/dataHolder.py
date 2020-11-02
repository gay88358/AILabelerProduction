
class DataHolder:
    def __init__(self, data):
        self.data = data

    def get_image_data(self):
        return self.data.get('image')

    def get_update_image_id(self):
        return self.get_image_data().get('id')

    def get_dataset_data(self):
        return self.data.get('dataset')
    
    def get_user_preferences(self):
        return self.data.get('user', {})

    def get_annotations_data_list(self):
        result = []
        for category in self.data.get('categories', []):
            self.get_enrich_annotation_data_list(category)
            annotation_data_list = category.get('annotations', [])
            result = result + annotation_data_list
        return result
    
    def get_enrich_annotation_data_list(self, category):
        # enrich category_id to annotation data
        annotation_data_list = category.get('annotations', [])
        for annotation_data in annotation_data_list:
            annotation_data['category_id'] = category['id']
        return annotation_data_list
    
    def get_categories_data(self):
        return self.data.get('categories', [])