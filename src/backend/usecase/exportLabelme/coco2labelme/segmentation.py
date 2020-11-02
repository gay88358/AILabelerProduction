
class Segmentation:
    def __init__(self, jsonDocument):
        self.document = jsonDocument
    
    def get_points_array(self, index):
        points = self.get_points(index)
        result = []
        for p in points:
            point_array = [p['x'], p['y']]
            result.append(point_array)
        return result

    def get_points(self, index):
        seg = self.segmentationAt(index)
        points = []
        point_size = int(len(seg) / 2)
        for i in range(0, point_size):
            x_index = i * 2
            y_index = i * 2 + 1
            points.append({ 'x': seg[x_index], 'y': seg[y_index] })
        return points

    def number_of_points_in_segmentationAt(self, index):
        return len(self.segmentationAt(index))
    
    def segmentationAt(self, index):
        return self.document[index]

    def get_segmentation_size(self):
        return len(self.document)

