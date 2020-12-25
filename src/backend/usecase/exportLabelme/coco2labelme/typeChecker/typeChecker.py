import math
import json

from ..segmentation import Segmentation

class TypeChecker:
    def __init__(self, document):
        self.document = document
        self.seg = None
        
    def is_given_type(self):
        # abstract method for overwrite
        pass

    def get_type(self):
        # abstract method for overwrite
        pass

    def get_points(self, index):
        return self.seg.get_points(index)

    def number_of_points_in_segmentationAt(self, index):
        return self.seg.number_of_points_in_segmentationAt(index)
     
   
    def setDocument(self, document):
        self.document = document
        self.seg = Segmentation(self.document['segmentation'])
    
    def get_points_array(self, index):
        return self.seg.get_points_array(index)

    def calculateEdge(self, p1, p2):
        return math.sqrt(math.pow(p1['x'] - p2['x'], 2) + math.pow(p1['y'] - p2['y'], 2))


class NormalTypeChecker(TypeChecker):
    def __init__(self):
        pass

    def is_given_type(self, index, document):
        if 'metadata' not in document:
            return False
        
        metadata = document['metadata']
        if 'Type' not in metadata:
            return False
        self.setDocument(document)
        return True

    def get_type(self):
        return self.document['metadata']['Type']

class CircleTypeChecker(TypeChecker):
    def __init__(self):
        pass

    def max_distance(self, first_point, index):
        distance = 0
        for second_point in self.get_points(index):
            if distance < self.calculateEdge(first_point, second_point):
                distance = self.calculateEdge(first_point, second_point)
        return distance

    def get_sum_distance(self, index):
        sumDistance = 0
        for first_point in self.get_points(index):
            distance = self.max_distance(first_point, index)
            if distance > 0:
                sumDistance += distance
        return sumDistance

    def get_weights(self, index):
        weights = []
        for first_point in self.get_points(index):
            distance = self.max_distance(first_point, index)
            if distance > 0:
                weights.append(distance)
        return weights
    
    def get_max_distance(self, index):
        maxDistance = 0
        for first_point in self.get_points(index):
            distance = self.max_distance(first_point, index)
            if distance > 0:
                if distance > maxDistance:
                    maxDistance = distance
        return maxDistance

    def is_given_type(self, index, document):
        ERROR_RATE = 0.1
        self.setDocument(document)
        avgDistance = self.get_avg_distance(index)
        errorConstraint = ERROR_RATE * avgDistance
        for w in self.get_weights(index):
            if abs(avgDistance - w) > errorConstraint:
                return False
        return True

    def get_avg_distance(self, index):
        return self.get_sum_distance(index) / len(self.get_weights(index))

    def get_type(self):
        return "circle"

if __name__ == "__main__":
    checker = CircleTypeChecker()
    coco_json_string = '{"images":[{"id":3,"dataset_id":2,"path":"/datasets/Dog/index.jpeg","width":198,"height":255,"file_name":"index.jpeg"}],"categories":[{"id":1,"name":"dog","supercategory":"","color":"#de19c9","metadata":{},"keypoint_colors":[]}],"annotations":[{"id":18,"image_id":3,"category_id":1,"segmentation":[[77.1,99.1,77.1,147.7,41.1,147.7,41.1,99.1]],"area":1764,"bbox":[41,99,36,49],"iscrowd":false,"isbbox":true,"color":"#af2704","keypoints":[],"metadata":{}},{"id":19,"image_id":3,"category_id":1,"segmentation":[[101.3,137.3,103.7,125.6,110.1,116,119.6,109.6,131.3,107.3,143,109.6,152.5,116,159,125.6,161.3,137.3,159,148.9,152.5,158.5,143,164.9,131.3,167.3,119.6,164.9,110.1,158.5,103.7,148.9],[64.1,55.3,77.5,45.8,91.4,54.9,133.9,49.2,137.4,65.3,127,83,90.5,96.5,83.2,78.7,68.9,70.9,67.1,59.6,65,57]],"area":5012,"bbox":[64,46,97,121],"iscrowd":false,"isbbox":false,"color":"#0fba58","keypoints":[],"metadata":{}}]}'
    coco_json = json.loads(coco_json_string)
    result = checker.is_given_type(0, coco_json['annotations'][1])
    assert result == True
    result = checker.is_given_type(1, coco_json['annotations'][1])
    assert result == False


class PolygonTypeChecker(TypeChecker):
    def __init__(self):
        pass

    def is_given_type(self, index, document):
        return True
    
    def get_type(self):
        return 'polygon'

class RectangleTypeChecker(TypeChecker):
    def __init__(self):
        pass
    
    def is_given_type(self, index, document):
        self.setDocument(document)
        return self.is_rectangle_type(index)

    def get_type(self):
        return "rectangle"

    def is_rectangle_type(self, index):
        if not self.number_of_points_in_segmentationAt(index) == 8:
            return False
        return self.edge_obey_rectangle_rule(self.get_points(index))

    def edge_obey_rectangle_rule(self, points):
        edges = []
        for i in range(0, len(points)):
            current_point = points[i]
            next_point_position = (i + 1) % len(points) 
            next_point = points[next_point_position]
            edges.append(self.calculateEdge(current_point, next_point))
        diagonal_edge = self.calculateEdge(points[0], points[2])
        sqaure_of_diagonal_edge = int(diagonal_edge * diagonal_edge)
        sqaure_of_first_and_second_edge = int(edges[0] * edges[0] + edges[1] * edges[1])
        return sqaure_of_diagonal_edge == sqaure_of_first_and_second_edge

    def calculateEdge(self, p1, p2):
        return math.sqrt(math.pow(p1['x'] - p2['x'], 2) + math.pow(p1['y'] - p2['y'], 2))

    