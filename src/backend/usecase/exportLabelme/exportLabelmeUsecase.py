import json
from .coco2labelme.coco2LabelmeConverter import CoCo2LabelmeConverter
from webserver.util import coco_util


class ExportLabelmeUsecase:
    def __init__(self):
        pass

    def execute(self, image_id):
        coco_document = coco_util.get_image_coco(image_id)
        coco_json_str = json.dumps(coco_document)
        labelme = CoCo2LabelmeConverter().convert_to_labelme(coco_json_str)
        return labelme
