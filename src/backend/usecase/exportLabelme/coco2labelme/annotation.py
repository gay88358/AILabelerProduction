from .typeChecker.typeChecker import *
from .segmentation import Segmentation
import numpy as np

# Metadata class is used to encapsulate metadata json data structure
# Encapsulate data structure can prevent the duplication of metadata json data structure
# When json data structure change, you only need to modify one place
# That is the application of object oriented programming's encapsulate concept  
class Metadata:
    def __init__(self, document):
        self.metadata_record = document['metadata']

    def get_score(self):
        return self.metadata_record.get('Score', 0)

    def get_manual_points(self):
        return self.metadata_record.get('manualPoints', [])

    def get_iou(self):
        return self.metadata_record.get('iou', [])
    
    def get_vertex_color(self):
        return self.metadata_record.get('vertex_color', [])
    
    def get_line_color(self):
        return self.metadata_record.get('line_color', [])
    
    def get_fill_color(self):
        return self.metadata_record.get('fill_color', [])
    
    def get_ignore_shapes(self):
        return self.metadata_record.get('IgnoreShapes', [])

    def get_type(self):
        return self.metadata_record.get('Type', "") 

class Annotation:
    def __init__(self, jsonDocument):
        self.document = jsonDocument
        self.metadata = Metadata(self.document)
        self.typeCheckers = []
        self.typeCheckers.append(NormalTypeChecker())
        self.typeCheckers.append(RectangleTypeChecker())
        self.typeCheckers.append(CircleTypeChecker())
        self.typeCheckers.append(PolygonTypeChecker())
        self.segmentation = Segmentation(self.document['segmentation'])
        
    def get_all_shapes(self):
        result = []
        for seg_index in range(0, self.get_segmentation_size()):
            result.append(self.get_shape(seg_index))
        return result

    def get_shape(self, index):
        shape = {   
                    'Type': self.get_shape_type(index),
                    'Score': self.metadata.get_score(),
                    'manualPoints': self.metadata.get_manual_points(),
                    'iou': self.metadata.get_iou(),
                    'vertex_color': self.metadata.get_vertex_color(),
                    'line_color': self.metadata.get_line_color(),
                    'fill_color': self.metadata.get_fill_color(),
                    'IgnoreShapes': self.metadata.get_ignore_shapes(),
                    'points': self.get_points_array(index),
                }
        self.append_attributes_to(shape)
        return shape

    def append_attributes_to(self, shape):
        shape['Attributes'] = {}

        isAttributes = ["Class", "Vim300_Code", "ID", "object_center", "rotation_center", "rotation_angle"]
        
        for key, value in self.document['metadata'].items():
            if key in isAttributes:
                shape['Attributes'][key] = value

    def get_shape_type(self, index):
        for checker in self.typeCheckers:
            if checker.is_given_type(index, self.document):
                return checker.get_type()
        raise Exception("Shape type is invalid")

    
    def get_points_array(self, index):
        result = self.segmentation.get_points_array(index)
        if self.metadata.get_type() == 'circle':
            # restore 2 points (diameter)
            result = self.restore_circle_type_points(result)
        return result

    def get_segmentation_size(self):
        return self.segmentation.get_segmentation_size()

    def restore_circle_type_points(self, shape):
        x1, y1 = shape[0]
        x2, y2 = shape[1]
        x3, y3 = shape[2]

        X = [[-2 * x1, -2 * y1, 1],
            [-2 * x2, -2 * y2, 1],
            [-2 * x3, -2 * y3, 1]]
        
        y = [[-(x1 ** 2 + y1 ** 2)],
            [-(x2 ** 2 + y2 ** 2)],
            [-(x3 ** 2 + y3 ** 2)]]

        X_i = np.linalg.inv(np.array(X))
        cx, cy, c = np.dot(X_i, y).reshape(-1)
        r = np.sqrt(cx ** 2 + cy ** 2 - c)

        return [[x1, y1], [2 * cx - x1, 2 * cy - y1]]
