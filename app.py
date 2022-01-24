#IMPORTAÇÕES DOS MÓDULOS
from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager 
from blacklist import BLACKLIST


#INSTANCIANDO A APLICAÇÃO
app = Flask(__name__)

#CRIO O BANCO DE DADOS SQLITE PELO SQLALCHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/banco_db'
#UMA CONFIGURAÇÃO PARA EVITAR APARECER AVISOS E SOBRECARREGAR O SISTEMA
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

#INSTANCIANDO A API
api = Api(app)

#INSTANCIANDO O JWT
jwt = JWTManager(app)

#COLOCO UM DECORATOR PARA ANTES DE FAZER A REQUISIÇÃO ELE CRIAR O BANCO
@app.before_first_request
def cria_banco():
    #CRIAR TUDO, BANCO, TABELA E COLUNAS
    banco.create_all()

#DECORADOR DO JWT PARA ADICIONAR O TOKEN EM UMA BLOCKLIST PARA INVALIDALO
@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

#DECORADOR PARA VERIFICAR O TOKEN
@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out'}), 401

#ADICIONO NA API OS RECURSOS DA URL PARA TER O RETORNO
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    #SE O PROGRAMA FOR RODADO PELO APP.PY ELE IMPORTA O SQL_ALCHEMY
    from sql_alchemy import banco
    #ESTOU LIGANDO O app = Flask(__name__) COM O BANCO INSTANCIADO EM SQL_ALCHEMY
    banco.init_app(app)
    app.run(debug=True)


#http://127.0.0.1:5000/