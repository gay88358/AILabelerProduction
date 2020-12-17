import pytest
from pymongo import MongoClient 
from usecase.idGenerator.annotationIdGenerator import *
    
@pytest.fixture()
def mongo_counters():
    mongo_host = 'localhost:27017/flask'
    factory = MongoClientFactory(mongo_host)
    mongo_counters = MongoengineCounters(factory)
    mongo_counters.drop()
    DEFAULT_KEY = 100
    mongo_counters.insert_annotation_model_record(DEFAULT_KEY)
    return mongo_counters

class TestCase:
    def test_generate_annotation_id_key_range(self, mongo_counters):
        cache_size = 40

        id_generator = AnnotationIdGenerator(cache_size, mongo_counters)
        
        assert id_generator.get_key_range() == [100, 140]
        assert id_generator.get_key_range() == [141, 181]
        assert id_generator.get_key_range() == [182, 222]