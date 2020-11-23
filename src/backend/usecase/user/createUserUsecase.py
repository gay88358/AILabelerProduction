


from database import UserModel
from config import Config
from ..util.result import Result


class CreateUserUsecase:

    def __init__(self, encryption_service):
        self.encryption_service = encryption_service
    
    def create(self, username, password, name, email):
        if self.can_not_register():
            return Result.failure(['Registration of new accounts is disabled.'])
    
        if UserModel.user_already_exists(username):
            user = UserModel.find_by_username(username)
            return Result.success(user.id)
        
        user = self.create_user(username, password, name, email)
        return Result.success(user.id)
    
    def can_not_register(self):
        not_allow_registration = not Config.ALLOW_REGISTRATION 
        contain_default_user = not self.no_user_exist()
        return not_allow_registration and contain_default_user
    
    def no_user_exist(self):
        users = UserModel.objects.count()
        return users == 0

    def create_user(self, username, password, name, email):
        if self.no_user_exist():
            return self.create_admin_user(username, password, name, email)
        else:
            return self.create_original_user(username, password, name, email)

    def create_admin_user(self, username, password, name, email):
        user = self.create_user_model(username, password, name, email)
        user.is_admin = True
        user.save()
        return user

    def create_original_user(self, username, password, name, email):
        user = self.create_user_model(username, password, name, email)
        user.save()
        return user
    
    def create_user_model(self, username, password, name, email):
        hash_password = self.encryption_service.hash_password(password)
        return UserModel.create(username, hash_password, name, email)