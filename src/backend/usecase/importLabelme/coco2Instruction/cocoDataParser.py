import json

class ParseResult:
    def __init__(self, category_data_list, annotation_data_list, user_metadata):
        self.category_data_list = category_data_list
        self.annotation_data_list = annotation_data_list
        self.user_metadata = user_metadata

    def get_user_metadata(self):
        return self.user_metadata

    def get_category_data_list(self):
        return self.category_data_list
    
    def get_annotation_data_list(self):
        return self.annotation_data_list

class CoCoDataParser:
    def __init__(self):
        self.json_document = {}

    def parse(self, json_string):
        self.set_json_document(json_string)

        return ParseResult(   
            self.parse_category(), 
            self.parse_annotation(),
            self.parse_user_metadata(),
        )

    def parse_user_metadata(self):
        return {}
    
    def to_user_metadata(self):
        return self.json_document['user_metadata']

    def parse_annotation(self):
        return self.to_annotation_list_data()

    def to_annotation_list_data(self):
        return list(
                    map(
                        lambda a: self.to_annotation_data(a), 
                        self.json_document['annotations']
                    )
                )

    def to_annotation_data(self, annotation_document):
        annotation_data = {
            "image_id": annotation_document['image_id'],
            "category_id": annotation_document['image_id'],
            "segmentation": annotation_document['segmentation'],
            "category_name": self.find_category_name_by(annotation_document['image_id']),
            "iscrowd": False,
            "isbbox":True,
            "bbox": annotation_document['bbox'],
            "color":"#af2704",
            "keypoints":[
            ],
        }
        self.append_metadata_to(annotation_data, annotation_document)
        return annotation_data
    
    def append_metadata_to(self, annotation_data, annotation_document):
        # annotation_document['metadata'] => { class: "defect_code" }
        annotation_data['metadata'] = annotation_document['metadata']
        annotation_data['metadata']['Type'] = annotation_document['Type']
        annotation_data['metadata']['Score'] = annotation_document['Score']
        annotation_data['metadata']['manualPoints'] = annotation_document['manualPoints']
        annotation_data['metadata']['iou'] = annotation_document['iou']
        annotation_data['metadata']['vertex_color'] = annotation_document['vertex_color']
        annotation_data['metadata']['line_color'] = annotation_document['line_color']
        annotation_data['metadata']['fill_color'] = annotation_document['fill_color']
        annotation_data['metadata']['IgnoreShapes'] = annotation_document['IgnoreShapes']

    def find_category_name_by(self, category_id):
        category = list(
                        filter(
                            lambda c: c['id'] == category_id , 
                            self.get_categories_document()
                        )
                    )
        return category[0]['name']

    def get_categories_document(self):
        return self.json_document['categories']

    def parse_category(self):
        categories_document = self.get_categories_document()
        return self.to_categories_list(categories_document)

    def to_categories_list(self, categories_document):
        return list(map(lambda c: self.to_categories_data(c), categories_document))

    def to_categories_data(self, categories_document):
        return {
            'id': categories_document['id'],
            'name': categories_document['name'],
            'supercategory': '',
            'color': '#de19c9',
            'metadata': {},
            'keypoint_colors': []
        }

    def set_json_document(self, json_string):
        self.json_document = json.loads(json_string)
