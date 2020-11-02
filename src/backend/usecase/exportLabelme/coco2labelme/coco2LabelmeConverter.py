

import json
from os import error
from .annotation import Annotation

class CoCo2LabelmeConverter:
    def __init__(self):
        self.json_document = None

    def convert_to_labelme(self, coco_json_string):
        self.set_json_document(coco_json_string)
        result = {}
        # collect parameter + composed method pattern
        self.appendLabelsTo(result)
        return result

    def set_json_document(self, coco_json_string):
        self.json_document = json.loads(coco_json_string)

    def appendLabelsTo(self, result):
        result['Labels'] = list(
            map(
                lambda c: {
                'Label': c['name'],
                'Shapes': self.get_shapes_by(c)
                }, 
                self.get_categories_document()
            )
        )

    def get_categories_document(self):
        return self.json_document['categories']
    
    def get_shapes_by(self, categoriy):
        result = []
        for annotation in self.get_annotations_by_categoriy(categoriy):
            for shape in annotation.get_all_shapes():
                result.append(shape)
        return result

    def get_annotations_by_categoriy(self, categoriy):
        return list(
            map(
                lambda a_json: Annotation(a_json),
                self.get_annotations_document_by(categoriy)
            )
        )

    def get_annotations_document_by(self, categoriy):
        return list(
            filter(
                lambda a: a['category_id'] == categoriy['id'],
                self.get_annotations_document()
            )
        )

    def get_annotations_document(self):
        return self.get_json_document()['annotations']

    def get_json_document(self):
        if self.json_document == None:
            raise error('Json Document is empty')
        return self.json_document
