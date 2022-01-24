from sql_alchemy import banco

#ESSE MODELO DE HOTEL VAI SER TAMBEM UM MODELO DE BANCO DE DADOS
class HotelModel(banco.Model):
    #DOU O NOME DA TABELA 
    __tablename__ = 'hoteis'

    #DOU AS COLUNAS DA TABELA
    hotel_id = banco.Column(banco.String(10),primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))

    #INSTANCIO A CLASSE
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade 

    #CONVERTE UM OBJETO DE CLASSE EM JSON
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }
    
    #CLS é class method, isso quer dizer que a função não precisa do self, ela esta dentro da classe mas não vai acessar nada da classe
    @classmethod
    def find_hotel(cls, hotel_id):
        #cls é a própria classe
        #query é a consulta na tabela
        #fintrando pelo id
        #pegando o primeiro resultado
        hotel = cls.query.filter_by(hotel_id= hotel_id ).first()
        if hotel:
            return hotel 
        return None

    #SALVA O HOTEL NO BANCO DE DADOS
    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    #ATUALIZA O HOTEL NO BANCO DE DADOS
    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade 
    
    #DELETA O HOTEL
    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()