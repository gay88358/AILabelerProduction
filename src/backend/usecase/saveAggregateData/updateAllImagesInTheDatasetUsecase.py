from database import (
    ImageModel,
)

class UpdateAllImagesInTheDatasetUsecase:
    def __init(self):
        self.data_holder = None

    def execute(self, num_annotations, data_holder):
        self.data_holder = data_holder
        self.update_all_images_in_the_dataset(
            self.data_holder.get_update_image_id(),
            num_annotations,
            self.data_holder.get_image_data())

    def update_all_images_in_the_dataset(self, image_id, num_annotations, image_data):
        images = self.find_all_images_in_the_dataset(image_id)
        for image in images:
            self.update_image(num_annotations, image_data, image)

    def find_all_images_in_the_dataset(self, image_id):
        image = ImageModel.objects.get(id=image_id)
        return ImageModel.objects(dataset_id=image.dataset_id)

    def update_image(self, num_annotations, image_data, image):
        image.update(
            set__metadata=image_data.get('metadata', {}),
            set__annotated=(num_annotations > 0),
            set__category_ids=image_data.get('category_ids', []),
            set__regenerate_thumbnail=True,
            set__num_annotations=num_annotations
        )
        self.generate_thumbnail(image)
    # seam point
    def generate_thumbnail(self, image_model):
        from webserver.util import thumbnails
        thumbnails.generate_thumbnail(image_model)
