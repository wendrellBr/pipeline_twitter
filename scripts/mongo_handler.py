from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

class MongoHandler:
    """
    Classe responsável pela conexão e inserção de dados no MongoDB.
    """

    def __init__(self):
        """
        Inicializa o manipulador do MongoDB carregando as configurações do arquivo .env.
        """
        load_dotenv(dotenv_path='config/.env')
        uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['tweets_db']
        self.collection = self.db['tweets']

    def insert_data(self, data):
        """
        Insere os dados no MongoDB.

        :param data: Dados a serem inseridos no MongoDB.
        """
        try:
            self.collection.insert_many(data)
            print("Dados inseridos com sucesso no MongoDB.")
        except Exception as e:
            print(f"Erro ao inserir dados no MongoDB: {e}")
            
  # Contar quantos documentos (tweets) existem na coleção
    
    def count_documents(self):
        """
        Conta quantos documentos existem na coleção.

        :return: Número de documentos.
        """
        try:
            tweet_count = self.collection.count_documents({})
            print(f"Total de tweets na coleção: {tweet_count}")
            return tweet_count
        except Exception as e:
            print(f"Erro ao contar documentos no MongoDB: {e}")
            return None
    

    def test_connection(self):
        """
        Testa a conexão com o MongoDB.
        """
        try:
            self.client.admin.command('ping')
            print("Conexão com MongoDB bem-sucedida.")
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            
    def close_connection(self):
        """
        Fecha a conexão com o MongoDB.
        """
        self.client.close()
        print("Conexão com MongoDB fechada.")
    
