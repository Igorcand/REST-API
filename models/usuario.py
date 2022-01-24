from sql_alchemy import banco

#ESSE MODELO DE USUÁRIO VAI SER TAMBEM UM MODELO DE BANCO DE DADOS
class UserModel(banco.Model):
    #DOU O NOME DA TABELA 
    __tablename__ = 'usuarios'

    #DOU AS COLUNAS DA TABELA
    user_id = banco.Column(banco.Integer,primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    #INSTANCIO A CLASSE
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha
        
    #CONVERTE UM OBJETO DE CLASSE EM JSON
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
            }
    
    #CLS é class method, isso quer dizer que a função não precisa do self, ela esta dentro da classe mas não vai acessar nada da classe
    @classmethod
    def find_user(cls, user_id):
        #cls é a própria classe
        #query é a consulta na tabela
        #fintrando pelo id
        #pegando o primeiro resultado
        user = cls.query.filter_by(user_id= user_id ).first()
        if user:
            return user 
        return None

    @classmethod
    #FILTRANDO NO BANCO DE DADOS SE EXISTE O LOGIN
    def find_by_login(cls, login):
        #cls é a própria classe
        #query é a consulta na tabela
        #fintrando pelo id
        #pegando o primeiro resultado
        user = cls.query.filter_by(login= login ).first()
        if user:
            return user 
        return None

    #SALVANDO O USUARIO
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    #DELETANDO O USUÁRIO
    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()