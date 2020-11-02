import datetime

from database import (
    AnnotationModel,
    SessionEvent,
    ImageModel
)

from .dataHolder import DataHolder

class UpdateAnnotationsUsecase:
    def __init__(self):
        self.data_hodler = None
        self.current_user = None

    def execute(self, data, current_user):
        self.data_hodler = DataHolder(data)
        self.current_user = current_user
        return self.update_all_annotations()

    def update_all_annotations(self):
        image_id_list = self.find_all_image_id_list()

        self.remove_annotations_in_all_images(image_id_list)

        self.add_annotations_to_all_images(image_id_list)

        return 10

    def find_all_image_id_list(self):
        image_id = self.data_hodler.get_update_image_id()
        image = ImageModel.find_by(image_id)
        images= ImageModel.find_images_by_dataset_id(image.dataset_id)
        return [img.id for img in images]

    def remove_annotations_in_all_images(self, image_id_list):
        for image_id in image_id_list:
            AnnotationModel.remove_by_image_id(image_id)

    def add_annotations_to_all_images(self, image_id_list):
        annotations_to_add = []
        for image_id in image_id_list:
            for annotation_data in self.data_hodler.get_annotations_data_list():
                annotations_to_add.append(self.create_annotation_from(annotation_data, image_id))

        if len(annotations_to_add) == 0:
            return
            
        AnnotationModel.objects.insert(annotations_to_add)

    def create_annotation_from(self, annotation_data, image_id):
        collect_annotation_data = {}
        self.append_events_ant_times_to(collect_annotation_data, annotation_data)
        self.append_papers_object_to(collect_annotation_data, annotation_data, image_id)
        self.append_other_data_to(collect_annotation_data, annotation_data, image_id)

        return AnnotationModel(
            image_id=image_id,
            category_id=annotation_data['category_id'],
            events=collect_annotation_data['events'],
            milliseconds=collect_annotation_data['milliseconds'],
            paper_object=collect_annotation_data['paper_object'],
            segmentation=collect_annotation_data['segmentation'],
            area=collect_annotation_data['area'],
            bbox=collect_annotation_data['bbox'],
            isbbox=collect_annotation_data['isbbox'],
            keypoints=collect_annotation_data['keypoints'],
            metadata=collect_annotation_data['metadata'],
            color=collect_annotation_data['color'],
        )

    def append_events_ant_times_to(self, collect_annotation_data, annotation_data):
        sessions, total_time = self.get_sessions_and_total_times(annotation_data, self.current_user)
        collect_annotation_data['events'] = sessions
        collect_annotation_data['milliseconds'] = total_time

    def get_sessions_and_total_times(self, annotation_data, current_user):
        # Paperjs objects are complex, so they will not always be passed. Therefor we update
        # the annotation twice, checking if the paperjs exists.
        sessions = []
        total_time = 0
        for session in annotation_data.get('sessions', []):
            date = datetime.datetime.fromtimestamp(int(session.get('start')) / 1e3)
            model = SessionEvent(
                user=current_user.get_username(),
                created_at=date,
                milliseconds=session.get('milliseconds'),
                tools_used=session.get('tools'),
            )
            total_time += session.get('milliseconds')
            sessions.append(model)
        return sessions, total_time
    
    def append_papers_object_to(self, collect_annotation_data, annotation_data, image_id):
        paperjs_object = annotation_data.get('compoundPath', [])
        if len(paperjs_object) == 2:
            image = ImageModel.find_by(image_id)
            width = image.width
            height = image.height
            segmentation, area, bbox = self.generate_coco_format_for_segment_data(width, height, paperjs_object)
            collect_annotation_data['paper_object'] = paperjs_object
            collect_annotation_data['segmentation'] = segmentation
            collect_annotation_data['area'] = area
            collect_annotation_data['bbox'] = bbox
            
    def append_other_data_to(self, collect_annotation_data, annotation_data, image_id):
        collect_annotation_data['isbbox'] = annotation_data.get('isbbox', False)
        collect_annotation_data['keypoints'] = annotation_data.get('keypoints', [])
        collect_annotation_data['metadata'] = annotation_data.get('metadata')
        collect_annotation_data['color'] = annotation_data.get('color')
        collect_annotation_data['image_id'] = image_id

    def generate_coco_format_for_segment_data(self, width, height, paperjs_object):
        from webserver.util import coco_util
        segmentation, area, bbox = coco_util.paperjs_to_coco(width, height, paperjs_object)
        return segmentation, area, bbox
