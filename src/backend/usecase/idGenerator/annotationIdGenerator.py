from pymongo import MongoClient 


class ConcurrencyReadException(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AnnotationRetryIdGenerator:
    def __init__(self, id_generator):
        self.id_generator = id_generator
    
    def get_key_range(self):
        count = 0
        RETRY_TIMES = 5
        while count < RETRY_TIMES:
            try:
                return self.id_generator.get_key_range()
            except ConcurrencyReadException:
                count += 1
        raise ValueError('Can not generate annotation key range')

class AnnotationIdGenerator:
    def __init__(self, cache_size, mongo_counters):
        self.cache_size = cache_size
        self.mongo_counters = mongo_counters
    
    def get_key_range(self):
        current_key = self.mongo_counters.find_current_annotation_model_id()
        self._update_current_key_with_cache_size(current_key)
        return [current_key, current_key + self.cache_size]

    def _update_current_key_with_cache_size(self, versionId):
        increment_size = self.cache_size + 1
        self.mongo_counters.increment_annotation_model_id(increment_size, versionId)


class MongoengineCounters:
    def __init__(self, mongo_factory):
        self.mongo_factory = mongo_factory
        self.collection_name = 'mongoengine.counters'

    def find_current_annotation_model_id(self):
        result = self._collection().find_one({'_id': "annotation_model.id"})
        return result['next']

    def increment_annotation_model_id(self, increment_size, versionId):
        result = self._collection().update_one({'_id': "annotation_model.id", 'next': versionId}, {'$inc': {'next': increment_size }})
        print(result.matched_count)
        concurrency_read = result.matched_count == 0
        if concurrency_read:
            raise ConcurrencyReadException('Two user attempt to update annotationId simultaneously, conflict happened')

    def update_annotation_model_id(self, id):
        self._collection().update_one({'_id': "annotation_model.id"}, {'$set': {'next': id }})

    def insert_annotation_model_record(self, id):
        self._collection().insert_one({ "_id" : "annotation_model.id", "next" : id })        

    def drop(self):
        self._collection().drop()

    def _collection(self):
        db = self._db()
        return db[self.collection_name]

    def _db(self):
        return self.mongo_factory.create_mongo_db_object()

class MongoClientFactory:
    def __init__(self, mongo_host):
        self.host, self.database_name = self._split_host_and_database_name(mongo_host)

    def create_mongo_db_object(self):
        client = MongoClient(
            host=[self.host],
            document_class=dict,
            tz_aware=False,
            connect=True
        )
        return client[self.database_name]
        
    def _split_host_and_database_name(self, mongo_host):
        last_delimiter_index = self._find_last_delimiter_index(mongo_host, '/')
        host = mongo_host[0: last_delimiter_index]
        index_skip_delimiter = last_delimiter_index + 1
        database_name = mongo_host[index_skip_delimiter:]
        return host, database_name

    def _find_last_delimiter_index(self, mongo_host, delimiter):
        for i in range(len(mongo_host) - 1, 0, -1):
            if mongo_host[i] == delimiter:
                return i
        raise ValueError('Given delimiter:{} is not found in the given host_url', delimiter)
    
__all__ = ['AnnotationIdGenerator', 'MongoengineCounters', 'MongoClientFactory', 'ConcurrencyReadException']