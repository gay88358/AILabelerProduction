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
                    'Score': self.get_score(),
                    'manualPoints': self.get_manual_points(),
                    'iou': self.get_iou(),
                    'vertex_color': self.get_vertex_color(),
                    'line_color': self.get_line_color(),
                    'fill_color': self.get_fill_color(),
                    'IgnoreShapes': self.get_ignore_shapes(),
                    'points': self.get_points_array(index),
                }
        self.append_attributes_to(shape)
        return shape
    
    def get_score(self):
        return self.get_metadata().get('Score', 0)

    def get_manual_points(self):
        return self.get_metadata().get('manualPoints', [])
    
    def get_iou(self):
        return self.get_metadata().get('iou', [])
    
    def get_vertex_color(self):
        return self.get_metadata().get('vertex_color', [])
    
    def get_line_color(self):
        return self.get_metadata().get('line_color', [])
    
    def get_fill_color(self):
        return self.get_metadata().get('fill_color', [])
    
    def get_ignore_shapes(self):
        return self.get_metadata().get('IgnoreShapes', [])

    def get_metadata(self):
        return self.document['metadata']

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
        if self.get_metadata().get('Type', "") == 'circle':
            # restore 2 points (diameter)
            sort_res = sorted(result)
            result = []
            result.append(sort_res[0])
            result.append(sort_res[-1])
        return result

    def get_segmentation_size(self):
        return self.segmentation.get_segmentation_size()
