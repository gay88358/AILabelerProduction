


from usecase.user.createUserUsecase import CreateUserUsecase
from ..utility.usecaseFixture import mongo_connection_setup

from ..utility.findHelper import Finder
from ..utility.objectMother import Mother

class MockEncryptionService:
    def __init__(self):
        pass
    def hash_password(self, password):
        return password

class TestCase:
    def test_create_user_with_result(self, mongo_connection_setup):
        # Arrange
        username = "WebUILabeler"
        password = "webUILabeler"
        name = "webUI"
        email = "gay88358@yahoo.com.tw"
        usecase = self.create_user_usecase()
        # Act
        result = usecase.create(username, password, name, email)
        # Assert
        assert result.is_success() == True
        user = Finder.find_user_by_id(result.value)
        assert user.name == name
        assert user.email == email

    def test_create_exist_user_is_invalid(self, mongo_connection_setup):
        # Arrange
        username = "WebUILabeler"
        password = "webUILabeler"
        name = "webUI"
        email = "gay88358@yahoo.com.tw"
        user_id = Mother.create_user(username, password)
        usecase = self.create_user_usecase()
        # Act
        result = usecase.create(username, password, name, email)
        # Assert
        assert result.is_success() == True
        assert result.value == user_id

    def create_user_usecase(self):
        return CreateUserUsecase(MockEncryptionService())