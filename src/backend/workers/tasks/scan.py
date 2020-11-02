from database import (
    ImageModel,
    TaskModel,
    DatasetModel
)

from celery import shared_task
from ..socket import create_socket
from .thumbnails import thumbnail_generate_single_image

import os


def find_task_by(task_id):
    return TaskModel.objects.get(id=task_id)
    
def find_dataset_by(dataset_id):
    return DatasetModel.objects.get(id=dataset_id)

def top_level_of_dataset(dataset):
    directory = dataset.directory
    toplevel = list(os.listdir(directory))
    return toplevel

def create_thumbnail_for_all_images():
    [thumbnail_generate_single_image.delay(image.id) for image in ImageModel.objects(regenerate_thumbnail=True).all()]


def create_image_by_path(path):
    created_image_size = 0
    if path.endswith(ImageModel.PATTERN):
        db_image = ImageModel.objects(path=path).first()
        if db_image is not None:
            return 0
        try:
            ImageModel.create_from_path(path, dataset.id).save()
            created_image_size += 1
            task.info(f"New file found: {path}")
        except:
            task.warning(f"Could not read {path}")
    return created_image_size

def create_images_in_the_files(root, files):
    count = 0
    for file in files:
        path = os.path.join(root, file)
        count += create_image_by_path(path)
    return count

def current_progress(current_task, task_size):
    progress = int(((current_task)/task_size)*100)
    return progress

def set_current_progress(dataset, root, socket):
    try:
        youarehere = top_level_of_dataset(dataset).index(root.split('/')[-1])
        task_size = len(top_level_of_dataset(dataset))
        current_progress(youarehere, task_size)
        task.set_progress(progress, socket=socket)
    except:
        pass


def create_images_in_the_directory(directory, dataset, socket):
    count = 0
    for root, dirs, files in os.walk(directory):
        set_current_progress(dataset, root, socket)
        if root.split('/')[-1].startswith('.'):
            continue
        
        count += create_images_in_the_files(root, files)
    return count

def scanning_directory_of_dataset(dataset, socket, task):
    directory = dataset.directory
    task.info(f"Scanning {directory}r")
    image_size = create_images_in_the_directory(directory, dataset, socket)
    create_thumbnail_for_all_images()
    task.info(f"Created {image_size} new image(s)")




def scanning_json_file_in_the_directory_of_dataset(dataset):
    # for root, dirs, files in os.walk(dataset.directory):
    from .jsonFileFinder import JsonFileFinder
    import json
    labelme_json = JsonFileFinder().find_json_in_the(dataset.directory)
    print(labelme_json)
    if labelme_json == "":
        return
    
    from usecase.importLabelmeAnnotationsUsecase import ImportLabelmeAnnotationsUseCase
    from usecase.addCategoriesToDatasetUseCase import AddCategoriesToDatasetUseCase

    usecase = ImportLabelmeAnnotationsUseCase(AddCategoriesToDatasetUseCase())
    images = ImageModel.find_images_by_dataset_id(dataset.id)
    
    for image in images:
        usecase.execute(dataset.id, image.id, json.dumps(labelme_json))



@shared_task    
def scan_dataset(task_id, dataset_id):
    task = find_task_by(task_id)
    task.update(status="PROGRESS")
    socket = create_socket()
    dataset = find_dataset_by(dataset_id)
    scanning_directory_of_dataset(dataset, socket, task)
    scanning_json_file_in_the_directory_of_dataset(dataset)
    task.set_progress(100, socket=socket)



__all__ = ["scan_dataset"]



####################### before refactor

# @shared_task
# def scan_dataset(task_id, dataset_id):

#     task = TaskModel.objects.get(id=task_id)
#     dataset = DatasetModel.objects.get(id=dataset_id)

#     task.update(status="PROGRESS")
#     socket = create_socket()
    
#     directory = dataset.directory
#     toplevel = list(os.listdir(directory))
#     task.info(f"Scanning {directory}")

#     count = 0
#     for root, dirs, files in os.walk(directory):

#         try:
#             youarehere = toplevel.index(root.split('/')[-1])
#             progress = int(((youarehere)/len(toplevel))*100)
#             task.set_progress(progress, socket=socket)
#         except:
#             pass

#         if root.split('/')[-1].startswith('.'):
#             continue
        
#         for file in files:
#             path = os.path.join(root, file)

#             if path.endswith(ImageModel.PATTERN):
#                 db_image = ImageModel.objects(path=path).first()

#                 if db_image is not None:
#                     continue

#                 try:
#                     ImageModel.create_from_path(path, dataset.id).save()
#                     count += 1
#                     task.info(f"New file found: {path}")
#                 except:
#                     task.warning(f"Could not read {path}")

#     [thumbnail_generate_single_image.delay(image.id) for image in ImageModel.objects(regenerate_thumbnail=True).all()]

#     task.info(f"Created {count} new image(s)")
#     task.set_progress(100, socket=socket)


# __all__ = ["scan_dataset"]