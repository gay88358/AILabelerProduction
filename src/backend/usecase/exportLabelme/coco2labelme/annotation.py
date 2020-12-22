from .typeChecker.typeChecker import *
from .segmentation import Segmentation

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


class Annotation:
    def __init__(self, jsonDocument):
        self.document = jsonDocument
        self.metadata = Metadata(self.document)
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
        return self.segmentation.get_points_array(index)

    def get_segmentation_size(self):
        return self.segmentation.get_segmentation_size()
