import pytest
from mongoengine.connection import disconnect
from mongoengine import connect
from database import ImageModel, CategoryModel, AnnotationModel, UserModel

@pytest.fixture()
def mongo_connection_setup():
    connect('test')
    ImageModel.objects.delete()
    AnnotationModel.objects.delete()
    CategoryModel.objects.delete()
    UserModel.objects.delete()
    yield
    disconnect('test')