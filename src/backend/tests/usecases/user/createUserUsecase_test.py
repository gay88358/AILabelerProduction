


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
        usecase = self.create_user_usecase()
        # Act
        result = usecase.create(self.get_user_name(), self.get_password(), self.get_name(), self.get_email())
        # Assert
        assert result.is_success()
        self.assert_user_create_successfully(result)

    def assert_user_create_successfully(self, result):
        user = Finder.find_user_by_id(result.value)
        assert user.name == self.get_name()
        assert user.email == self.get_email()

    def test_create_exist_user_is_invalid(self, mongo_connection_setup):
        # Arrange
        username = self.get_user_name()
        password = self.get_password()
        name = self.get_name()
        email = self.get_email()
        user_id = Mother.create_user(username, password)
        usecase = self.create_user_usecase()
        # Act
        result = usecase.create(username, password, name, email)
        # Assert
        assert result.is_success()
        assert result.value == user_id

    def create_user_usecase(self):
        return CreateUserUsecase(MockEncryptionService())
    
    def get_user_name(self):
        return "WebUILabeler"
    
    def get_password(self):
        return "webUILabeler"
    
    def get_name(self):
        return "webUI"
    
    def get_email(self):
        return "gay88358@yahoo.com.tw"