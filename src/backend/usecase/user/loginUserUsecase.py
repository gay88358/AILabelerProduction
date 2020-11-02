from database import UserModel

class LoginUserUsecase:

    def __init__(self, login_user_callback, encryption_service, logger, json_prepare) -> None:
        self.login_user_callback = login_user_callback
        self.encryption_service = encryption_service
        self.logger = logger
        self.json_prepare = json_prepare

    def execute(self, username, password):
        user = self.find_user_by_username(username)
        if user is None or not self.password_is_correct(user, password):
            return {'success': False, 'message': 'Could not authenticate user'}, 400
        
        # self.login_user_callback(user)
        self.logger.info(f'User {user.username} has LOGIN')
        return {'success': True, 'user': self.json_prepare.prepare_user_json(user)}

    def find_user_by_username(self, username):
        user = UserModel.objects(username__iexact=username).first()
        return user

    def password_is_correct(self, user, password):
        return self.encryption_service.is_same_password(user.password, password)
