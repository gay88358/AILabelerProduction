
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

    def get_all_categories(self):
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
        result = list(filter(lambda c: c["name"] == label_name, self.get_all_categories()))
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
        self.append_user_metadata_to(result)
        self.appendCategoriesTo(result)
        self.appendAnnotationsTo(result)
        return result

    def append_user_metadata_to(self, result):
        # user_metadata = {}
        # user_metadata['vertexColor'] = self.labelme_document['vertexColor']
        # user_metadata['lineColor'] = self.labelme_document['lineColor']
        # user_metadata['fillColor'] = self.labelme_document['fillColor']
        # user_metadata['globalAttributes'] = self.labelme_document['globalAttributes']
        # user_metadata['UserName'] = self.labelme_document['UserName']
        # user_metadata['UserIp'] = self.labelme_document['UserIp']
        # user_metadata['CreatedTime'] = self.labelme_document['CreatedTime']
        # user_metadata['ModifiedTime'] = self.labelme_document['ModifiedTime']
        # result['user_metadata'] = user_metadata
        pass
    
    def set_labelme_document(self, labelme_json_string):
        self.labelme_document = json.loads(labelme_json_string)
        self.labels = Labels(self.labelme_document['Labels'])

    def appendCategoriesTo(self, result):
        result["categories"] = self.labels.get_all_categories()

    def appendAnnotationsTo(self, result):
        result["annotations"] = []
        for label_name in self.labels.get_all_label_names():
            for index, shape in enumerate(self.find_shapes_by_label_name(label_name)):
                shape_id = index
                annotation = self.shape_to_annotation(shape, shape_id, label_name)
                result["annotations"].append(annotation)

    def find_shapes_by_label_name(self, label_name):
        return self.labels.find_shapes_by_label_name(label_name)

    def shape_to_annotation(self, shape, shape_id, label_name):
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
        contain_defect_code = 'class' in shape['Attributes']
        if contain_defect_code:
            annotation['metadata'] = {
                "class": shape['Attributes']['class']
            }
        else:
            annotation['metadata'] = {}

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

def assert_categories(result):
    assert result['categories'][0] == { 'id': 0, 'name': 'wire' }
    assert result['categories'][1] == { 'id': 1, 'name': 'bond_rec' }
    assert result['categories'][2] == { 'id': 2, 'name': 'wire_2' }
    assert result['categories'][3] == { 'id': 3, 'name': 'bond_90' }
    assert result['categories'][4] == { 'id': 4, 'name': 'bottle' }

def assert_annotaions(result):
    assert len(result['annotations']) == 37

def assert_coco_format(result):
    assert result == {'categories': [{'id': 0, 'name': 'wire'}, {'id': 1, 'name': 'bond_rec'}, {'id': 2, 'name': 'wire_2'}, {'id': 3, 'name': 'bond_90'}, {'id': 4, 'name': 'bottle'}], 'annotations': [{'id': 0, 'image_id': 0, 'segmentation': [[947.0, 1127.0, 943.0, 1126.0, 922.0, 1151.0, 922.0, 1156.0, 925.0, 1155.0, 945.0, 1133.0]], 'bbox': [922.0, 1126.0, 25.0, 30.0]}, {'id': 1, 'image_id': 0, 'segmentation': [[852.0, 1124.0, 846.0, 1130.0, 839.0, 1143.0, 834.0, 1149.0, 831.0, 1157.0, 835.0, 1157.0, 847.0, 1141.0, 854.0, 1129.0, 854.0, 1126.0]], 'bbox': [831.0, 1124.0, 23.0, 33.0]}, {'id': 2, 'image_id': 0, 'segmentation': [[1031.0, 1114.0, 1025.0, 1118.0, 1012.0, 1134.0, 996.0, 1151.0, 999.0, 1154.0, 1005.0, 1150.0, 1025.0, 1129.0, 1033.0, 1119.0]], 'bbox': [996.0, 1114.0, 37.0, 40.0]}, {'id': 3, 'image_id': 0, 'segmentation': [[398.0, 1107.0, 396.0, 1109.0, 396.0, 1112.0, 419.0, 1153.0, 423.0, 1157.0, 428.0, 1159.0, 427.0, 1154.0, 409.0, 1124.0, 404.0, 1113.0]], 'bbox': [396.0, 1107.0, 32.0, 52.0]}, {'id': 4, 'image_id': 0, 'segmentation': [[7.0, 898.0, 8.0, 915.0, 9.0, 902.0]], 'bbox': [7.0, 898.0, 2.0, 17.0]}, {'id': 5, 'image_id': 0, 'segmentation': [[1003.0, 803.0, 1004.0, 813.0, 1018.0, 850.0, 1031.0, 891.0, 1039.0, 912.0, 1043.0, 917.0, 1046.0, 915.0, 1045.0, 907.0, 1031.0, 870.0, 1011.0, 808.0, 1007.0, 802.0]], 'bbox': [1003.0, 802.0, 43.0, 115.0]}, {'id': 6, 'image_id': 0, 'segmentation': [[1039.0, 779.0, 1039.0, 783.0, 1045.0, 787.0, 1134.0, 821.0, 1139.0, 820.0, 1139.0, 818.0, 1136.0, 815.0, 1123.0, 811.0, 1078.0, 792.0, 1064.0, 788.0, 1045.0, 779.0]], 'bbox': [1039.0, 779.0, 100.0, 42.0]}, {'id': 7, 'image_id': 0, 'segmentation': [[7.0, 779.0, 8.0, 784.0, 58.0, 803.0, 96.0, 819.0, 103.0, 819.0, 102.0, 815.0, 95.0, 811.0, 82.0, 807.0, 44.0, 791.0]], 'bbox': [7.0, 779.0, 96.0, 40.0]}, {'id': 8, 'image_id': 0, 'segmentation': [[7.0, 583.0, 8.0, 590.0, 75.0, 627.0, 88.0, 631.0, 88.0, 627.0, 83.0, 623.0]], 'bbox': [7.0, 583.0, 81.0, 48.0]}, {'id': 9, 'image_id': 0, 'segmentation': [[699.0, 579.0, 695.0, 579.0, 580.0, 635.0, 536.0, 653.0, 525.0, 659.0, 523.0, 663.0, 528.0, 664.0, 633.0, 617.0, 696.0, 586.0, 699.0, 583.0]], 'bbox': [523.0, 579.0, 176.0, 85.0]}, {'id': 10, 'image_id': 0, 'segmentation': [[799.0, 559.0, 795.0, 559.0, 792.0, 562.0, 779.0, 582.0, 734.0, 659.0, 591.0, 891.0, 588.0, 899.0, 590.0, 901.0, 592.0, 901.0, 596.0, 897.0, 611.0, 874.0, 705.0, 716.0, 796.0, 568.0]], 'bbox': [588.0, 559.0, 211.0, 342.0]}, {'id': 11, 'image_id': 0, 'segmentation': [[316.0, 547.0, 319.0, 549.0, 330.0, 550.0, 451.0, 551.0, 622.0, 557.0, 626.0, 555.0, 624.0, 551.0, 527.0, 547.0, 392.0, 545.0, 327.0, 542.0, 318.0, 543.0]], 'bbox': [316.0, 542.0, 310.0, 15.0]}, {'id': 12, 'image_id': 0, 'segmentation': [[795.0, 534.0, 757.0, 577.0, 737.0, 604.0, 578.0, 799.0, 495.0, 895.0, 495.0, 900.0, 499.0, 899.0, 516.0, 882.0, 582.0, 805.0, 757.0, 588.0, 779.0, 563.0, 797.0, 539.0, 797.0, 536.0]], 'bbox': [495.0, 534.0, 302.0, 366.0]}, {'id': 13, 'image_id': 0, 'segmentation': [[795.0, 510.0, 790.0, 512.0, 769.0, 533.0, 675.0, 633.0, 578.0, 732.0, 506.0, 808.0, 442.0, 872.0, 408.0, 903.0, 405.0, 907.0, 407.0, 911.0, 411.0, 910.0, 437.0, 887.0, 535.0, 788.0, 608.0, 710.0, 796.0, 515.0]], 'bbox': [405.0, 510.0, 391.0, 401.0]}, {'id': 14, 'image_id': 0, 'segmentation': [[807.0, 459.0, 807.0, 463.0, 819.0, 471.0, 833.0, 477.0, 963.0, 550.0, 1111.0, 630.0, 1123.0, 635.0, 1125.0, 631.0, 1120.0, 627.0, 1017.0, 573.0, 855.0, 483.0, 829.0, 470.0, 819.0, 463.0, 811.0, 459.0]], 'bbox': [807.0, 459.0, 318.0, 176.0]}, {'id': 15, 'image_id': 0, 'segmentation': [[314.0, 451.0, 317.0, 455.0, 339.0, 461.0, 427.0, 481.0, 591.0, 523.0, 604.0, 525.0, 621.0, 530.0, 626.0, 528.0, 623.0, 524.0, 613.0, 521.0, 583.0, 515.0, 565.0, 509.0, 512.0, 497.0, 468.0, 485.0, 377.0, 463.0, 368.0, 462.0, 321.0, 449.0, 315.0, 449.0]], 'bbox': [314.0, 449.0, 312.0, 81.0]}, {'id': 16, 'image_id': 0, 'segmentation': [[1125.0, 358.0, 1118.0, 357.0, 1079.0, 367.0, 1028.0, 377.0, 829.0, 423.0, 814.0, 425.0, 809.0, 427.0, 807.0, 431.0, 811.0, 433.0, 822.0, 431.0, 834.0, 427.0, 848.0, 425.0, 1017.0, 385.0, 1114.0, 365.0, 1123.0, 362.0]], 'bbox': [807.0, 357.0, 318.0, 76.0]}, {'id': 17, 'image_id': 0, 'segmentation': [[89.0, 355.0, 87.0, 353.0, 82.0, 353.0, 30.0, 367.0, 7.0, 371.0, 7.0, 378.0, 86.0, 359.0]], 'bbox': [7.0, 353.0, 82.0, 25.0]}, {'id': 18, 'image_id': 0, 'segmentation': [[1127.0, 267.0, 1125.0, 264.0, 1122.0, 264.0, 1048.0, 293.0, 1028.0, 299.0, 951.0, 329.0, 919.0, 343.0, 911.0, 345.0, 884.0, 357.0, 766.0, 400.0, 760.0, 403.0, 759.0, 407.0, 765.0, 408.0, 780.0, 403.0, 1004.0, 314.0, 1122.0, 271.0]], 'bbox': [759.0, 264.0, 368.0, 144.0]}, {'id': 19, 'image_id': 0, 'segmentation': [[91.0, 260.0, 83.0, 260.0, 63.0, 269.0, 10.0, 288.0, 7.0, 290.0, 7.0, 295.0, 86.0, 267.0, 91.0, 263.0]], 'bbox': [7.0, 260.0, 84.0, 35.0]}, {'id': 20, 'image_id': 0, 'segmentation': [[633.0, 254.0, 630.0, 257.0, 630.0, 365.0, 631.0, 400.0, 635.0, 403.0, 637.0, 400.0, 637.0, 258.0, 636.0, 255.0]], 'bbox': [630.0, 254.0, 7.0, 149.0]}, {'id': 21, 'image_id': 0, 'segmentation': [[419.0, 251.0, 415.0, 248.0, 322.0, 251.0, 320.0, 255.0, 322.0, 257.0, 404.0, 256.0, 414.0, 255.0]], 'bbox': [320.0, 248.0, 99.0, 9.0]}, {'id': 22, 'image_id': 0, 'segmentation': [[947.0, 88.0, 942.0, 91.0, 887.0, 162.0, 715.0, 357.0, 693.0, 385.0, 638.0, 448.0, 637.0, 451.0, 639.0, 453.0, 643.0, 451.0, 724.0, 356.0, 891.0, 167.0, 943.0, 101.0, 949.0, 91.0]], 'bbox': [637.0, 88.0, 312.0, 365.0]}, {'id': 23, 'image_id': 0, 'segmentation': [[855.0, 87.0, 852.0, 88.0, 848.0, 93.0, 844.0, 102.0, 797.0, 179.0, 651.0, 398.0, 637.0, 421.0, 635.0, 427.0, 639.0, 428.0, 643.0, 424.0, 704.0, 328.0, 808.0, 173.0, 856.0, 92.0]], 'bbox': [635.0, 87.0, 221.0, 341.0]}, {'id': 24, 'image_id': 0, 'segmentation': [[1035.0, 79.0, 1031.0, 79.0, 1013.0, 100.0, 962.0, 154.0, 864.0, 253.0, 639.0, 472.0, 639.0, 477.0, 643.0, 477.0, 915.0, 211.0, 1003.0, 120.0, 1033.0, 85.0]], 'bbox': [639.0, 79.0, 396.0, 398.0]}, {'id': 25, 'image_id': 0, 'segmentation': [[399.0, 71.0, 400.0, 76.0, 409.0, 94.0, 418.0, 109.0, 464.0, 199.0, 471.0, 209.0, 474.0, 208.0, 475.0, 205.0, 473.0, 199.0, 447.0, 153.0, 407.0, 76.0, 403.0, 70.0]], 'bbox': [399.0, 70.0, 76.0, 139.0]}, {'id': 0, 'image_id': 1, 'segmentation': [[534.0, 6.0, 613.0, 6.0, 613.0, 117.0, 534.0, 117.0]], 'bbox': [534.0, 6.0, 79.0, 111.0]}, {'id': 1, 'image_id': 1, 'segmentation': [[438.5979957119707, 5.05413427187267, 517.5162910497177, 1.462106852132223, 522.5633169179605, 112.34730663048532, 443.6450215802137, 115.93933405022585]], 'bbox': [438.0, 1.0, 84.0, 114.0]}, {'id': 0, 'image_id': 2, 'segmentation': [[806.0, 580.0, 804.0, 583.0, 825.0, 618.0, 893.0, 721.0, 899.0, 727.0, 901.0, 727.0, 902.0, 723.0, 852.0, 649.0, 813.0, 586.0, 809.0, 581.0]], 'bbox': [804.0, 580.0, 98.0, 147.0]}, {'id': 0, 'image_id': 3, 'segmentation': [[227.0, 627.0, 227.0, 649.0, 229.0, 653.0, 247.0, 653.0, 274.0, 668.0, 318.0, 668.0, 327.0, 663.0, 330.0, 655.0, 330.0, 620.0, 326.0, 615.0, 318.0, 612.0, 272.0, 611.0, 249.0, 622.0, 241.0, 624.0, 231.0, 623.0]], 'bbox': [227.0, 611.0, 103.0, 57.0]}, {'id': 1, 'image_id': 3, 'segmentation': [[227.0, 723.0, 227.0, 745.0, 229.0, 749.0, 247.0, 749.0, 274.0, 764.0, 318.0, 764.0, 327.0, 759.0, 330.0, 751.0, 330.0, 716.0, 326.0, 711.0, 318.0, 708.0, 272.0, 707.0, 249.0, 718.0, 241.0, 720.0, 231.0, 719.0]], 'bbox': [227.0, 707.0, 103.0, 57.0]}, {'id': 2, 'image_id': 3, 'segmentation': [[228.0, 531.0, 228.0, 553.0, 230.0, 557.0, 248.0, 557.0, 275.0, 572.0, 319.0, 572.0, 328.0, 567.0, 331.0, 559.0, 331.0, 524.0, 327.0, 519.0, 319.0, 516.0, 273.0, 515.0, 250.0, 526.0, 242.0, 528.0, 232.0, 527.0]], 'bbox': [228.0, 515.0, 103.0, 57.0]}, {'id': 0, 'image_id': 4, 'segmentation': [[650.9999823126033, 7.064379656178318, 651.0005403826242, 11.06437961724805, 653.0009589156748, 14.064100553039879, 652.0031912054911, 30.064239914824043, 640.0066792599127, 55.06591388157267, 640.0112833375855, 88.06591356039792, 643.0133760709663, 103.06549486189374, 646.0140736292948, 108.06507626071516, 690.014212718567, 109.05893748075232, 694.0137941271211, 106.05837943992913, 698.0123989131384, 96.05782146723385, 699.007655308228, 62.0576822806359, 698.0063996604134, 53.057821885734256, 689.0041674679228, 37.059077699002415, 683.0016562112239, 19.059914979220025, 685.0005400517169, 11.059636022070094, 688.0001214700036, 8.059217498752105, 687.9997029174879, 5.059217527949784, 652.9998427756329, 6.064100630900413]], 'bbox': [640.0, 5.0, 59.0, 104.0]}, {'id': 1, 'image_id': 4, 'segmentation': [[746.8602701361999, 7.392045897265177, 746.8741429732776, 11.392021840241767, 748.8845355725741, 14.38506737893539, 747.9400329351407, 30.388439360111136, 736.0268103379464, 55.429907514947786, 736.1412612438371, 88.42970904450465, 739.1932663401108, 103.41921420285854, 742.2105893436903, 108.40877950377103, 786.2137929257021, 109.25617228166084, 790.2033642408705, 106.24231748735076, 794.1686580911529, 96.22850479283159, 795.0507329617369, 62.2252410682612, 794.019525092568, 53.22876340583332, 784.96408787256, 37.260073517351714, 778.9016961912456, 19.280991029573613, 780.8739384885786, 11.274102725081605, 783.8635158180027, 8.263716140040913, 783.8531111901946, 5.263734182808463, 748.8567898984188, 6.385115492982209]], 'bbox': [736.0, 5.0, 59.0, 104.0]}, {'id': 2, 'image_id': 4, 'segmentation': [[842.9549544508808, 7.278326756373417, 842.9515322692718, 11.278325292457282, 844.948964901107, 14.280035285324686, 843.9352765406501, 30.279173884257887, 831.9138922973423, 55.26889818995505, 831.885659299068, 88.2688861126469, 834.8728250200973, 103.2714472591681, 837.868546195149, 108.27401206547972, 881.8676745466692, 109.31165569719957, 885.8702397189597, 106.31507897674567, 889.878793709066, 96.31850481814502, 890.9078818867634, 62.319372806834394, 889.9155821613627, 53.31852055524348, 880.92927418161, 37.310826502287796, 874.9446761947247, 19.30569981749693, 876.9515198259846, 11.307413836133719, 879.9540853642543, 8.309981570277557, 879.956652000461, 5.309982668214673, 844.955809264325, 6.280038213156956]], 'bbox': [831.0, 5.0, 59.0, 104.0]}, {'id': 3, 'image_id': 4, 'segmentation': [[938.8798675902749, 8.176677535014164, 938.866117786345, 12.176653902805839, 940.8557936172933, 15.18351108061455, 939.8008003096259, 31.17997910079876, 927.7149349316888, 56.13858198770703, 927.6014990492671, 89.13838702198836, 930.5499195603737, 104.14861075415456, 933.5327145813051, 109.15889356684158, 977.5290171760312, 110.31013550201851, 981.5393058967702, 107.3239030301047, 985.5736567743866, 97.33771191455537, 986.6905241997388, 63.34135023930861, 985.7214671666331, 54.33796596079486, 976.7765195548213, 38.30712343078585, 970.8384291208185, 20.286605069828454, 972.8659169125742, 12.293527236210082, 975.8762115413654, 9.303857313313756, 975.8865238943129, 6.303875037469993, 940.8832932251532, 7.1835583450312015]], 'bbox': [927.0, 6.0, 59.0, 104.0]}, {'id': 4, 'image_id': 4, 'segmentation': [[1034.722714835337, 6.3391165617982494, 1034.8154320076023, 10.33804185817064, 1036.8844325349874, 13.290877244317329, 1036.2555698999554, 29.309757722873258, 1024.838276337496, 54.58119234199654, 1025.6031930086842, 87.57232603706888, 1028.9500763769581, 102.49875801926646, 1032.065166814569, 107.42787676053308, 1076.0765243677317, 107.40771918970847, 1080.0059117849053, 104.31580804516392, 1083.7730441506146, 94.22577763196762, 1083.9846795104531, 60.21173331973591, 1082.776334548763, 51.23733069596429, 1073.4078839428644, 35.45024314807148, 1066.9922687231121, 17.594155072793512, 1068.8062970267679, 9.54994589391606, 1071.735953119848, 6.481214042437841, 1071.6664152406493, 3.4820200701585122, 1036.698998190457, 5.293026651572518]], 'bbox': [1024.0, 3.0, 59.0, 104.0]}]}
    assert_annotaions(result)
    




