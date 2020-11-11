
import json
from json import load

from .bboxCalculator import BBoxCalculator

class Labels:
    def __init__(self, labels_document):
        self.labels_document = labels_document
    
    def find_shapes_by_label_name(self, label_name):
        result = []
        for label_and_shapes_document in self.labels_document:
            if label_and_shapes_document['Label'] == label_name:
                for s in label_and_shapes_document['Shapes']:
                    result.append(s)
        return result

    def categories(self):
        result = []
        for index, label_name in enumerate(self.get_all_label_names()):
            categories = {
                "id": index,
                "name": label_name
            }
            result.append(categories)
        return result

    def get_all_label_names(self):
        return list(map(lambda l: l['Label'], self.labels_document))
    
    def find_category_by_label_name(self, label_name):
        result = list(filter(lambda c: c["name"] == label_name, self.categories()))
        if len(result) == 0:
            raise ValueError('Invalid label name, category not found!')
        return result[0]
    

class Labelme2CoCoConverter:
    def __init__(self, image_bound_size):
        self.labelme_document = {}
        self.image_bound_size = image_bound_size

    def convert(self, labelme_json_string):
        self.set_labelme_document(labelme_json_string)

        result = {}
        self.appendCategoriesTo(result)
        self.appendAnnotationsTo(result)
        return result
    
    def set_labelme_document(self, labelme_json_string):
        self.labelme_document = json.loads(labelme_json_string)
        self.labels = Labels(self.labelme_document['Labels'])

    def appendCategoriesTo(self, result):
        result["categories"] = self.labels.categories()

    def appendAnnotationsTo(self, result):
        result["annotations"] = []
        for label_name in self.labels.get_all_label_names():
            for index, shape in enumerate(self.labels.find_shapes_by_label_name(label_name)):
                shape_id = index
                annotation = self.to_annotation(shape, shape_id, label_name)
                result["annotations"].append(annotation)

    def to_annotation(self, shape, shape_id, label_name):
        category = self.labels.find_category_by_label_name(label_name)
        
        annotation = {
            "id": shape_id,
            "image_id": category['id'],
            "segmentation": [self.get_segmentation(shape)],
            "bbox": self.calculate_bbox(shape)
        }
        self.append_defect_code_to(annotation, shape)
        self.append_type_code_to(annotation, shape)
        self.append_labels_metadata_to(annotation, shape)
        return annotation
    
    def calculate_bbox(self, shape):
        return BBoxCalculator().calculate_bbox(shape['points'], self.image_bound_size)

    def append_defect_code_to(self, annotation, shape):
        annotation['metadata'] = {}
        attributes = shape['Attributes']
        for key, value in attributes.items():
            annotation['metadata'][key] = value

    def append_type_code_to(self, annotation, shape):
        annotation['Type'] = shape.get('Type', "")

    def append_labels_metadata_to(self, annotation, shape):
        annotation['Score'] = shape.get('Score', 0)
        annotation['manualPoints'] = shape.get('manualPoints', [])
        annotation['iou'] = shape.get('iou', -1)
        annotation['vertex_color'] = shape.get('vertex_color', [])
        annotation['line_color'] = shape.get('line_color', [])
        annotation['fill_color'] = shape.get('fill_color', [])
        annotation['IgnoreShapes'] = shape.get('IgnoreShapes', [])
        
    def get_segmentation(self, shape):
        result = []
        for point in shape['points']:
            x = point[0]
            y = point[1]
            result.append(x)
            result.append(y)
        return result
    
    def find_all_shapes(self):
        labels_document = self.labelme_document['Labels']
        result = []
        for label_and_shapes_document in labels_document:
            shapes = label_and_shapes_document['Shapes']
            for s in shapes:
                result.append(s)
        return result
