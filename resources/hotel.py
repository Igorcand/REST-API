#IMPORTAÇÕES DOS MÓDULOS
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import mysql.connector as mysql


#ESTA FUNÇÃO CRIA OS PARAMETROS PADRÕES,PARA CASO NÃO SEJA PASSANONADA A ELA, ELA TEM IS PARÂMETROS DE MODO QUE SEJA EXIBIDO TUDO
def normilize_path_params(cidade=None, 
                         estrelas_min=0, 
                         estrelas_max=5,
                         diaria_min=0, 
                         diaria_max=10000, 
                         limit=50, 
                         offset=0, **dados):   
    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit':limit,
            'offset':offset
        }
    return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limit':limit,
            'offset':offset
        }

#path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400
path_params=reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

#ESSA CLASSE É PARA EXIBIR HOTEIS, TUDO OU COM FILTROS DESEJADOS
class Hoteis(Resource):
    def get(self):
        #PARA USAR O FILTROS, TEMOS QUE CRIAR UMA CONEXÃO COM O BANCO DE DADOS E PROCURAR DENTRO DELE

        
        connection = mysql.connect(host='localhost', user='root', password='', database='banco_db')
        cursor = connection.cursor()
        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normilize_path_params(**dados_validos)
        if not parametros.get('cidade'):
            consulta = 'SELECT * FROM hoteis WHERE (estrelas >= ? AND estrelas <= ?) AND (diaria >= ? AND diaria <= ?) AND LIMIT= ? AND OFFSET = ? VALUES (%s, %s, %s, %s, %s, %s)'
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)
        else:
            consulta = 'SELECT * FROM hoteis WHERE (estrelas >= ? AND estrelas <= ?) AND (diaria >= ? AND diaria <= ?) AND cidade = ? AND LIMIT = ? AND OFFSET =? VALUES (%s, %s, %s, %s, %s, %s)'
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta, tupla)        
        hoteis = []
        for linha in resultado:
            hoteis.append({
            'hotel_id': linha[0],
            'nome': linha[1],
            'estrelas': linha[2],
            'diaria': linha[3],
            'cidade': linha[4]
        })
        return {'hoteis': hoteis}

#ESSA CLASSE É USADA PARA USAR OS RECURSOS GET, POST, PUT E DELETE
class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type = str, required=True, help="The field 'nome' cannot be left blank")
    atributos.add_argument('estrelas', type = float, required=True, help="The field 'estrelas' cannot be left blank")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')   
    #O COMANDO GET É PARA PROCURAR HOTEIS ESPECIFICOS DE ACORDO COM O HOTEL_ID
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404  
    #ESSE DECORADOR É PARA VERIFICAR SE A PESSOA FEZ LOGIN, CASO ELA ESTEJA LOGADA, COM O TOKEN DE ACESSO VÁLIDO, ELA PODE UTILIZAR O COMANDO POST
    @jwt_required()
    #O COMANDO POST É PARA ADICIONAR HOTEI
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': "Hotel_id '{}' already exists".format(hotel_id)}, 400 
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json()

    #ESSE DECORADOR É PARA VERIFICAR SE A PESSOA FEZ LOGIN, CASO ELA ESTEJA LOGADA, COM O TOKEN DE ACESSO VÁLIDO, ELA PODE UTILIZAR O COMANDO PUT
    @jwt_required()
    #O COMANDO PUT É PARA ATUALIZAR UM HOTEL JÁ EXISTENTE OU CRIAR UM NOVO
    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json(), 201

    #ESSE DECORADOR É PARA VERIFICAR SE A PESSOA FEZ LOGIN, CASO ELA ESTEJA LOGADA, COM O TOKEN DE ACESSO VÁLIDO, ELA PODE UTILIZAR O COMANDO DELETE
    @jwt_required()
    #O COMANDO DELETE É PARA EXCLUIR UM HOTEL
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to delete hotel.'}, 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found'}, 404
