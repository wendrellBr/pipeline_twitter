import asyncio
from twitter_client import TwitterClient
from tweet_processor import TweetProcessor
from mongo_handler import MongoHandler

async def main():
    # Coleta dos tweets
    query = 'Elon Musk min_faves:200 until:2024-12-31 since:2024-01-01'
    client = TwitterClient(query, min_tweets=100)
    await client.fetch_and_save_tweets()

    # Processamento dos tweets
    processor = TweetProcessor('data/tweets.csv')
    processor.load_data()
    processor.clean_data()

    # Obter os dados processados
    df = processor.get_data()

    # Manipulação dos dados no MongoDB
    mongo_handler = MongoHandler()
    mongo_handler.test_connection()

    # Inserir os dados no MongoDB
    data_dict = df.to_dict(orient='records')
    mongo_handler.insert_data(data_dict)
    
    # Contar quantos documentos (tweets) existem na coleção
    mongo_handler.count_documents()

    mongo_handler.close_connection() # Fechar a conexão com o MongoDB

if __name__ == "__main__":
    asyncio.run(main())
