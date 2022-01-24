#IMPORTAÇÕES DOS MÓDULOS
from textwrap import indent
from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

#REQUISIÇÃO DOS ATRIBUTOS LOGIN E SENHA
atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")


#ESSA CLASSE É PARA PROCURAR UM USUARIO OU DELETER O USUÁRIO
class User(Resource):
    #/usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    #ESSE DECORADOR É PARA VERIFICAR SE A PESSOA FEZ LOGIN, CASO ELA ESTEJA LOGADA, COM O TOKEN DE ACESSO VÁLIDO, ELA PODE DELETAR O USUÁRIO
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurred trying to delete hotel.'}, 500
            return {'message': 'User deleted.'}
        return {'message': 'User not found'}, 404


#ESSA CLASSE É PARA CADASTRAR O USUÁRIO
class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()
        if UserModel.find_by_login(dados['login']):
            return {'message': "the login '{}' already exists.".format(dados['login'])}       
        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created successfully'}, 201

#ESSA CLASSE É PARA FAZER O LOGIN
class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])
        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access token': token_de_acesso}, 200
        return {'message': 'The username or password are incorrect'}, 401

#ESSA CLASSE É PARA FAZER O LOGOUT
class UserLogout(Resource):
    #ESSE DECORADOR É PARA VERIFICAR SE A PESSOA FEZ LOGIN, CASO ELA ESTEJA LOGADA, COM O TOKEN DE ACESSO VÁLIDO, ELA PODE FAZER O LOGOUT
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']  #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}, 200

