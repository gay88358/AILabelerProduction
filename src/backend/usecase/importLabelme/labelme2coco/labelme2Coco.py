
import json
from json import load
import math
import numpy as np

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

class Shape:

    SCORE = 'Score'
    TYPE = 'Type'
    MANUAL_POINTS = 'manualPoints'
    IOU = 'iou'
    VERTEX_COLOR = 'vertex_color'
    LINE_COLOR = 'line_color'
    FILL_COLOR = 'fill_color'
    IGNORE_SHAPES = 'IgnoreShapes'

    def __init__(self, shape_document):
        self.shape_document = shape_document

    def get_attributes(self):
        return self.shape_document['Attributes']

    def get_type(self):
        return self.shape_document.get('Type', "")

    def get_shape_metadata(self):
        result = {}
        result[Shape.SCORE] = self.shape_document.get(Shape.SCORE, 0)
        result[Shape.MANUAL_POINTS] = self.shape_document.get(Shape.MANUAL_POINTS, [])
        result[Shape.IOU] = self.shape_document.get(Shape.IOU, -1)
        result[Shape.VERTEX_COLOR] = self.shape_document.get(Shape.VERTEX_COLOR, [])
        result[Shape.LINE_COLOR] = self.shape_document.get(Shape.LINE_COLOR, [])
        result[Shape.FILL_COLOR] = self.shape_document.get(Shape.FILL_COLOR, [])
        result[Shape.IGNORE_SHAPES] = self.shape_document.get(Shape.IGNORE_SHAPES, [])
        return result
    
    @staticmethod
    def get_shape_metadata_keys():
        return [
            Shape.TYPE,
            Shape.SCORE,
            Shape.MANUAL_POINTS,
            Shape.IOU,
            Shape.VERTEX_COLOR,
            Shape.LINE_COLOR,
            Shape.FILL_COLOR,
            Shape.IGNORE_SHAPES
        ]

    def get_points(self):
        return self.shape_document['points']

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
        shape_object = self.create_shape_object(shape)
        annotation = {
            "id": shape_id,
            "image_id": self.labels.find_category_by_label_name(label_name)['id'],
            "segmentation": [self.get_segmentation(shape_object)],
            "bbox": self.calculate_bbox(shape_object)
        }
        self.append_metadata_to(annotation, shape_object)
        self.append_type_code_to(annotation, shape_object)
        self.append_labels_metadata_to(annotation, shape_object)
        return annotation
    
    def calculate_bbox(self, shape):
        return BBoxCalculator().calculate_bbox(
            shape.get_points(), 
            self.image_bound_size
            )

    def append_metadata_to(self, annotation, shape):
        annotation['metadata'] = {}

        for key, value in shape.get_attributes().items():
            annotation['metadata'][key] = value

    def append_type_code_to(self, annotation, shape):
        annotation['Type'] = shape.get_type()

    def create_shape_object(self, shape_document):
        return Shape(shape_document)

    def append_labels_metadata_to(self, annotation, shape):
        for key, value in shape.get_shape_metadata().items():
            annotation[key] = value
        
    def get_segmentation(self, shape):    
        if shape.get_type() == 'circle':
            result = self.process_circle_type_points(shape)
            return list(np.array(result).flat)
        else: # the shape except for the circle generate by original pointss
            return self.generate_points(shape)
    
    def generate_points(self, shape):
        result = []
        for point in shape.get_points():
            x = point[0]
            y = point[1]
            result.append(x)
            result.append(y)
        return result

    def process_circle_type_points(self, shape):
        result = []
        x1, y1 = shape.get_points()[0]
        x2, y2 = shape.get_points()[1]
        r = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1/2) / 2
        o_x = (x1 + x2) / 2
        o_y = (y1 + y2) / 2
        for i in range(3):
            x = o_x + math.cos(math.pi / 1.5 * i) * r
            y = o_y + math.sin(math.pi / 1.5 * i) * r
            result.append([x, y])
        return result

    def find_all_shapes(self):
        labels_document = self.labelme_document['Labels']
        result = []
        for label_and_shapes_document in labels_document:
            shapes = label_and_shapes_document['Shapes']
            for s in shapes:
                result.append(s)
        return result
