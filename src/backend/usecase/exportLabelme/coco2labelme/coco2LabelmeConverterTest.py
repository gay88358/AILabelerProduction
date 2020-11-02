

import json
import math

from .coco2LabelmeConverter import CoCo2LabelmeConverter
from usecase.util.jsonHelper import JsonHelper

def expected(result):
    assert result == {'Labels': [{'Shapes': [{'Attributes': {}, 'points': [[93.6, 35.7], [93.6, 59.7], [62.8, 59.7], [62.8, 35.7]], 'Type': 'rectangle'}, {'Attributes': {}, 'points': [[164.4, 47.3], [164.4, 84.1], [125.2, 84.1], [125.2, 47.3]], 'Type': 'rectangle'}], 'Label': u'dog'}, {'Shapes': [{'Attributes': {}, 'points': [[54.4, 108.5], [92.4, 120.9], [81.2, 142.9], [48, 149.7], [46.4, 116.1], [54, 108.9]], 'Type': 'polygon'}, {'Attributes': {}, 'points': [[109.6, 135.7], [112, 124], [118.4, 114.5], [127.9, 108], [139.6, 105.7], [151.3, 108], [160.8, 114.5], [167.2, 124], [169.6, 135.7], [167.2, 147.4], [160.8, 156.9], [151.3, 163.3], [139.6, 165.7], [127.9, 163.3], [118.4, 156.9], [112, 147.4]], 'Type': 'circle'}, {'Attributes': {}, 'points': [[188.8, 117.7], [191.1, 106], [197.6, 96.5], [207.1, 90], [218.8, 87.7], [230.5, 90], [240, 96.5], [246.4, 106], [248.8, 117.7], [246.4, 129.4], [240, 138.9], [230.5, 145.3], [218.8, 147.7], [207.1, 145.3], [197.6, 138.9], [191.1, 129.4]], 'Type': 'circle'}, {'Attributes': {}, 'points': [[192.4, 34.1], [194.7, 22.4], [201.2, 12.9], [210.7, 6.5], [222.4, 4.1], [234.1, 6.5], [243.6, 12.9], [250, 22.4], [252.4, 34.1], [250, 45.8], [243.6, 55.3], [234.1, 61.8], [222.4, 64.1], [210.7, 61.8], [201.2, 55.3], [194.7, 45.8]], 'Type': 'circle'}], 'Label': u'mydoc'}]}

def load_coco_json():
    return JsonHelper.load_json_string("/Users/koushiken/Desktop/formatConverter/CoCo2LabelMeConverter/coco2labelme/multiple_category_coco.json")

if __name__ == "__main__":
    converter = CoCo2LabelmeConverter()
    coco_json_string = load_coco_json()
    result = converter.convert_to_labelme(coco_json_string) 
    expected(result)
