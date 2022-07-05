from flask import Blueprint
from flask import render_template
#from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')

# @simple_page.route('/', defaults={'page': 'index'})
# @simple_page.route('/<page>')
# def show(page):
#     try:
#         return render_template(f'pages/{page}.html')
#     except TemplateNotFound:
#         abort(404)


@simple_page.route('/')
def home():
    return render_template('index.html')

# import json
# from flask import request, Blueprint
# from flask_restplus import Resource
# from flask_jwt_extended import create_access_token, create_refresh_token, \
#     jwt_required

# from app.app import bcrypt, Api
# from app.auth_api.models import User

#blueprint = Blueprint('auth', __name__)
#api = Api(blueprint)

# @app.route('/')
# def home():
#     return render_template('index.html')



# @api.route('/login')
# class Login(Resource):
#     @api.doc(description='Метод для авторизации пользователей в системе',
#              responses={200: 'OK', 404: 'Login error'},
#              params={
#                  'login': 'Логин пользователя',
#                  'password': 'Пароль пользователя'
#              })
#     def post(self):
#         request_params = json.loads(request.data)
#
#         user = User.get(login=request_params.get('login'))
#         pswd_check = bcrypt.check_password_hash(user.password,
#                                                 request_params['password'])
#         if user and pswd_check:
#             access_token = create_access_token(identity=user.id)
#             refresh_token = create_refresh_token(identity=user.id)
#
#             return user.build_response_body(access_token, refresh_token), 200
#         api.abort(404, 'Ошибка авторизации!'
#                        ' Проверьте правильность логина и пароля')
#
#
# @api.route('/logout')
# class Logout(Resource):
#     @api.doc(description='Метод для выхода пользователя из системы')
#     @jwt_required
#     def get(self):
#         return {'message', 'You were logged out'}
#
#
# @api.route('/sing_up')
# class SingUP(Resource):
#     @api.doc(description='Метод для регистрации нового пользователя',
#              responce={200: 'OK', 401: 'Registration Error'},
#              params={'login': 'Логин пользователя',
#                      'password': 'Пароль пользователя',
#                      'first_name': 'Имя',
#                      'last_name': 'Фамилия',
#                      'email': 'Email',
#                      'roles': 'Список ролей в проекте',
#                      })
#     def post(self):
#         request_params = json.loads(request.data)
#         request_params['password'] = bcrypt.generate_password_hash(
#             request_params['password']).decode('utf-8')
#         user = User.create(**request_params)
#         access_token = create_access_token(identity=user.id)
#         refresh_token = create_refresh_token(identity=user.id)
#         if user:
#             return {'user': user.build_response_body(access_token,
#                                                      refresh_token)}, 200
#         api.abort(401, 'Ошибка регистрации')
