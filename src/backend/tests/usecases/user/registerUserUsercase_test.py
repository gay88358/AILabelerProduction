



from usecase.user.registerUserUsecase import RegisterUserUsecase

from ..utility.usecaseFixture import (
    mongo_connection_setup
)

from ..utility.findHelper import (
    Finder
)

from ..utility.objectMother import (
    FakeDataset, Mother
)

class MockEncryptionService:
    def hash_password(self, password):
        return password

class MockJsonPrepare:
    def prepare_user_json(self, user):
        pass

class TestCase:

    def test_user_register(self, mongo_connection_setup):
        # Arrange
        username = "test user"
        password = "my password"
        name = "adsf"
        email = "xxx3@gmail.com"
        usecase = self.create_register_user_usecase()
        # Act
        usecase.execute(username, password, name, email)
        self.assert_user_registered(username, password, name, email)

    def test_register_user_with_exist_username(self, mongo_connection_setup):
        # Arrange
        username = "test user"
        password = "my password"
        name = "adsf"
        email = "xxx3@gmail.com"
        Mother.create_user(username, password)
        usecase = self.create_register_user_usecase()
        # Act
        result = usecase.execute(username, password, name, email)
        # Assert
        assert result[0] == {'success': False, 'message': 'Username already exists.'}

    def create_register_user_usecase(self):
        def login_user_callback(user):
            pass
        return RegisterUserUsecase(login_user_callback, MockEncryptionService(), MockJsonPrepare())

    def assert_user_registered(self, username, password, name, email):
        user = Finder.find_user()
        assert user.username == username
        assert user.password == password
        assert user.name == name
        assert user.email == email

