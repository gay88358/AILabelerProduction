import pytest
from usecase.idGenerator.annotationIdGenerator import *
    
@pytest.fixture()
def mongo_counters():
    mongo_host = 'localhost:27017/flask'
    factory = MongoClientFactory(mongo_host)
    mongo_counters = FakeMongoengineCounters(factory)
    mongo_counters.drop()
    DEFAULT_KEY = 100
    mongo_counters.insert_annotation_model_record(DEFAULT_KEY)
    return mongo_counters

class FakeMongoengineCounters(MongoengineCounters):
    
    def __init__(self, factory):
        super().__init__(factory)
        self.is_concurrency_read = False

    def find_current_annotation_model_id(self):
        if self.is_concurrency_read:
            return 100
        return super().find_current_annotation_model_id()

    def should_happen_concurrency_read(self):
        self.is_concurrency_read = True

class StubAnnotationIdGenerator:
    def __init__(self):
        self.invoke_times = 0

    def get_key_range(self):
        self.invoke_times += 1
        raise ConcurrencyReadException

class TestCase:

    def test_retry_when_concurrency_read_happened(self, mongo_counters):
        stub = StubAnnotationIdGenerator()
        retry_generator = AnnotationRetryIdGenerator(stub)
        try:
            retry_generator.get_key_range()
        except ValueError:
            pass
        self.assert_retry_times(stub)
        
    def assert_retry_times(self, stub):
        assert stub.invoke_times == 5

    def test_read_concurrency_should_throw_exception(self, mongo_counters):
        cache_size = 40
        mongo_counters.should_happen_concurrency_read()
        id_generator = AnnotationIdGenerator(cache_size, mongo_counters)
        id_generator.get_key_range()
        try:
            id_generator.get_key_range()
            self.fail()
        except ConcurrencyReadException as e:
            pass
    
    def fail(self):
        assert 1 == 2

    def test_generate_annotation_id_key_range(self, mongo_counters):
        cache_size = 40

        id_generator = AnnotationIdGenerator(cache_size, mongo_counters)
        assert id_generator.get_key_range() == [100, 140]
        assert id_generator.get_key_range() == [141, 181]
        assert id_generator.get_key_range() == [182, 222]
