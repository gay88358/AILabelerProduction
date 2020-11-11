from .typeChecker.typeChecker import *

from .segmentation import Segmentation

class Annotation:
    def __init__(self, jsonDocument):
        self.document = jsonDocument
        self.typeCheckers = []
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
                    'Score': self.document['metadata']['Score'],
                    'manualPoints': self.document['metadata']['manualPoints'],
                    'iou': self.document['metadata']['iou'],
                    'vertex_color': self.document['metadata']['vertex_color'],
                    'line_color': self.document['metadata']['line_color'],
                    'fill_color': self.document['metadata']['fill_color'],
                    'IgnoreShapes': self.document['metadata']['IgnoreShapes'],
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
        return self.segmentation.get_points_array(index)

    def get_segmentation_size(self):
        return self.segmentation.get_segmentation_size()
