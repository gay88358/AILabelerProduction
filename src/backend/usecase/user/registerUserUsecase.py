from database import UserModel
from config import Config

class RegisterUserUsecase:

    def __init__(self, login_user_callback, encryption_service, json_prepare):
        self.login_user_callback = login_user_callback
        self.encryption_service = encryption_service
        self.json_prepare = json_prepare

    def execute(self, username, password, name, email):
        if self.can_not_register():
            return {'success': False, 'message': 'Registration of new accounts is disabled.'}, 400
        
        if UserModel.user_already_exists(username):
            return {'success': False, 'message': 'Username already exists.'}, 400
        
        user = self.create_user(username, password, name, email)

        return {
            'success': True, 
            'user': self.json_prepare.prepare_user_json(user)
        }
    
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
        user = UserModel()
        user.username = username
        user.password = self.encryption_service.hash_password(password)
        user.name = name
        user.email = email
        user.is_admin = True
        user.save()
        return user

    def create_original_user(self, username, password, name, email):
        user = UserModel()
        user.username = username
        user.password = self.encryption_service.hash_password(password)
        user.name = name
        user.email = email
        user.save()
        return user
    