from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restplus import Namespace, Resource, reqparse
from usecase.user.encryptionService import EncryptionService
from usecase.user.jsonPrepare import JsonPrepare

from config import Config
from ..util.query_util import fix_ids

import logging
logger = logging.getLogger('gunicorn.error')

api = Namespace('user', description='User related operations')

register = reqparse.RequestParser()
register.add_argument('username', required=True, location='json')
register.add_argument('password', required=True, location='json')
register.add_argument('email', location='json')
register.add_argument('name', location='json')

login = reqparse.RequestParser()
login.add_argument('password', required=True, location='json')
login.add_argument('username', required=True, location='json')

set_password = reqparse.RequestParser()
set_password.add_argument('password', required=True, location='json')
set_password.add_argument('new_password', required=True, location='json')


@api.route('/')
class User(Resource):
    @login_required
    def get(self):
        """ Get information of current user """
        if Config.LOGIN_DISABLED:
            return current_user.to_json()

        user_json = fix_ids(current_user)
        del user_json['password']

        return {'user': user_json}


@api.route('/password')
class UserPassword(Resource):
    @login_required
    @api.expect(register)
    def post(self):
        """ Set password of current user """
        args = set_password.parse_args()

        if current_user.is_same_password(args.get('password')):
            current_user.change_password(args.get('new_password'), generate_password_hash)
            return {'success': True}

        return {'success': False, 'message': 'Password does not match current passowrd'}, 400

@api.route('/register')
class UserRegister(Resource):
    @api.expect(register)
    def post(self):
        """ Creates user """
        args = register.parse_args()

        username = args.get('username')
        password = args.get('password')
        name = args.get('name')
        email = args.get('email')
        from usecase.user.registerUserUsecase import RegisterUserUsecase
        return RegisterUserUsecase(login_user, EncryptionService(), JsonPrepare()).execute(username, password, name, email)

@api.route('/login')
class UserLogin(Resource):
    @api.expect(login)
    def post(self):
        """ Logs user in """
        args = login.parse_args()
        username = args.get('username')
        password = args.get('password')
        from usecase.user.loginUserUsecase import LoginUserUsecase
        return LoginUserUsecase(login_user, EncryptionService(), logger, JsonPrepare()).execute(username, password)

@api.route('/logout')
class UserLogout(Resource):
    @login_required
    def get(self):
        """ Logs user out """
        logger.info(f'User {current_user.get_username()} has LOGOUT')
        logout_user()
        return {'success': True}

