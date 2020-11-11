import json
from usecase.importLabelme.labelme2coco.labelme2Coco import Shape


class ParseResult:
    def __init__(self, category_data_list, annotation_data_list):
        self.category_data_list = category_data_list
        self.annotation_data_list = annotation_data_list

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
            self.parse_annotation()
        )

    def parse_category(self):
        return list(
                    map(
                        lambda c: self.to_categories_record(c), 
                        self.get_categories_document()
                    )
                )

    def to_categories_record(self, categories_document):
        return {
            'id': categories_document['id'],
            'name': categories_document['name'],
            'supercategory': '',
            'color': '#de19c9',
            'metadata': {},
            'keypoint_colors': []
        }

    def parse_annotation(self):
        return list(
                    map(
                        lambda a: self.to_annotation_record(a), 
                        self.json_document['annotations']
                    )
                )

    def to_annotation_record(self, annotation_document):
        image_id = annotation_document['image_id']
        annotation_data = {
            "image_id": image_id,
            "category_id": image_id,
            "segmentation": annotation_document['segmentation'],
            "category_name": self.find_category_name_by(image_id),
            "iscrowd": False,
            "isbbox":True,
            "bbox": annotation_document['bbox'],
            "color":"#af2704",
            "keypoints":[
            ],
        }
        self.append_metadata_to(annotation_data, annotation_document)
        return annotation_data
    
    def find_category_name_by(self, category_id):
        result = list(
                        filter(
                            lambda c: c['id'] == category_id , 
                            self.get_categories_document()
                        )
                    )
        return result[0]['name']

    def get_categories_document(self):
        return self.json_document['categories']
 
    def append_metadata_to(self, annotation_data, annotation_document):
        # Attributes metadata
        annotation_data['metadata'] = annotation_document['metadata']
        # Additional shape data
        # for key in Shape.get_shape_metadata_keys():
        #     annotation_data['metadata'][key] = annotation_document[key]
        annotation_data['metadata']['Type'] = annotation_document['Type']
        annotation_data['metadata']['Score'] = annotation_document['Score']
        annotation_data['metadata']['manualPoints'] = annotation_document['manualPoints']
        annotation_data['metadata']['iou'] = annotation_document['iou']
        annotation_data['metadata']['vertex_color'] = annotation_document['vertex_color']
        annotation_data['metadata']['line_color'] = annotation_document['line_color']
        annotation_data['metadata']['fill_color'] = annotation_document['fill_color']
        annotation_data['metadata']['IgnoreShapes'] = annotation_document['IgnoreShapes']
    
    def set_json_document(self, json_string):
        self.json_document = json.loads(json_string)
