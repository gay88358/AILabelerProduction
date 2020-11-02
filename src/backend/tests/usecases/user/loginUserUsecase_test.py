



from database.users import UserModel
from usecase.user.loginUserUsecase import LoginUserUsecase

from ..utility.usecaseFixture import (
    mongo_connection_setup
)

from ..utility.objectMother import (
    Mother
)

from ..utility.findHelper import (
    Finder
)



class StubEncryptionService:
    def is_same_password(self, user_password, password):
        return True

class Logger:
    def info(self, message):
        pass

class JsonPrepare:
    def prepare_user_json(self, user):
        pass

class TestCase:


    def test_find_by_username(self, mongo_connection_setup):
        Mother.create_user("123", "123")
        user = UserModel.find_by_username("123")

        assert user.username == "123"
        assert user.username == "123"

        

    def test_user_login(self, mongo_connection_setup):
        # Arrange
        user_login = []
        def login_user(user):
            user_login.append('login')
        
        username = "test user"
        password = "my password"
        self.register_user(username, password)
        usecase = LoginUserUsecase(
            login_user,
            StubEncryptionService(),
            Logger(),
            JsonPrepare()
        )
        # Act
        usecase.execute(username, password)
        # Assert
        self.assert_user_created(username, password)
    
    def register_user(self, username, password):
        return Mother.create_user(username, password)

    def assert_user_created(self, username, password):
        user = Finder.find_user()
        assert user.username == username
        assert user.password == password



if __name__ == "__main__":
    print('hello')