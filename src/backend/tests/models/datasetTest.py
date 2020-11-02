from database import (
    DatasetModel
)

from ..usecases.findHelper import Finder
from ..usecases.objectMother import Mother
from ..usecases.usecaseFixture import mongo_connection_setup



class TestCase:

    def test_change_category_id_list_of_dataset(self, mongo_connection_setup):
        
        assert 1 == 2