
import PIL.Image
import PIL.ImageDraw
import numpy as np

class BBoxCalculator:    
    def calculate_bbox(self, point_array, image_bound_size):
        bbox_list = self.getbbox(point_array, image_bound_size)
        return self.to_float(bbox_list)

    def to_float(self, bbox_list):
        return list(map(float, bbox_list))

    def getbbox(self,points, image_bound_size):
        polygons = points
        mask = self.polygons_to_mask(image_bound_size, polygons)
        return self.mask2box(mask)

    def polygons_to_mask(self, img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = PIL.Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        PIL.ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

    def mask2box(self, mask):
        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]

        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x
        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)
        return [left_top_c, left_top_r, right_bottom_c-left_top_c, right_bottom_r-left_top_r]


def get_image_bound_size():
    return [1344, 743]

def test_calculate_bbox_of_rectangle():
    calculator = BBoxCalculator()
    image_bound_size = get_image_bound_size()
    point_array = [[340.5, 218.1],
                    [340.5,288.8],
                    [240.8,288.8],
                    [240.8,218.1]]
    assert [240, 218, 100, 70] == calculator.calculate_bbox(point_array, image_bound_size) 

    point_array = [[646.4, 408.1], 
                [646.4, 499.3], 
                [567.2, 499.3], 
                [567.2, 408.1]]  
    assert [567, 408, 79, 91] == calculator.calculate_bbox(point_array, image_bound_size) 

def test_calculate_bbox_of_circle():
    calculator = BBoxCalculator()
    image_bound_size = get_image_bound_size()
    point_array = [[646.4, 408.1], [646.4, 499.3], [567.2, 499.3], [567.2, 408.1]]
    assert [567, 408, 79, 91] == calculator.calculate_bbox(point_array, image_bound_size) 

def test_calculate_bbox_of_polygon():
    calculator = BBoxCalculator()
    image_bound_size = get_image_bound_size()
    point_array = [
        [727.3,
        284.6],
        [651.3,
        510.9],
        [435.7,
        510.9],
        [375.6,
        305.9],
        [384.4,
        176.8],
        [446.3,
        111.5],
        [508.1,
        175.1],
        [520.5,
        180.4],
        [511.7,
        176.8]]
    assert [375.0, 111.0, 352.0, 399.0] == calculator.calculate_bbox(point_array, image_bound_size) 


if __name__ == "__main__":
    test_calculate_bbox_of_rectangle()
    test_calculate_bbox_of_circle()
    test_calculate_bbox_of_polygon()
    