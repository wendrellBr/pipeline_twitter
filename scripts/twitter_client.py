import asyncio
import os
import json
import csv
from datetime import datetime
from random import randint
from twikit import Client, TooManyRequests
from dotenv import load_dotenv

class TwitterClient:
    """
    Classe para interagir com a API do Twitter e obter tweets baseados em uma query.
    """
    
    def __init__(self, query, min_tweets=10):
        """
        Inicializa a classe com a query de busca e a quantidade mínima de tweets a serem obtidos.
        
        :param query: A query para buscar tweets.
        :param min_tweets: A quantidade mínima de tweets a serem obtidos.
        """
        self.query = query
        self.min_tweets = min_tweets
        self.client = None
        self.tweet_count = 0
        self.tweets = None

    async def get_tweets(self):
        """
        Obtém tweets da API do Twitter. Se já houver tweets carregados, obtém a próxima página.
        
        :return: Tweets obtidos.
        """
        if self.tweets is None:
            print(f'{datetime.now()} - Obtendo tweets...')
            self.tweets = await self.client.search_tweet(self.query, product='Top', count=500 )
        else:
            wait_time = randint(5, 10)  # Tempo de espera aleatório para evitar bloqueio
            print(f'{datetime.now()} - Obtendo próximos tweets após {wait_time} segundos...')
            await asyncio.sleep(wait_time)
            self.tweets = await self.tweets.next()
        return self.tweets

    async def authenticate(self):
        """
        Autentica o cliente na API do Twitter usando variáveis de ambiente e carrega cookies.
        """
        load_dotenv(dotenv_path='config/.env')  # Carregar variáveis de ambiente
        username = os.getenv("NAME") 
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")

        self.client = Client(language='pt_BR')
        await self.client.login(auth_info_1=username, auth_info_2=email, password=password)
        
        # Salvar e carregar cookies para manter a sessão ativa
        self.client.save_cookies('config/cookies.json')
        self.client.load_cookies('config/cookies.json')

    async def fetch_and_save_tweets(self):
        """
        Obtém tweets e salva os resultados em arquivos CSV e JSON.
        """
        await self.authenticate()

        # Criar arquivo CSV
        with open('data/tweets.csv', 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Tweet_count', 'Username', 'Text', 'Created_At', 'Retweets', 'Likes'])

        json_data = []

        # Obter tweets até atingir a quantidade mínima de tweets
        while self.tweet_count < self.min_tweets:
            try:
                self.tweets = await self.get_tweets()
            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                print(f'{datetime.now()} - Limite de taxa alcançado. Esperando até {rate_limit_reset}')
                wait_time = rate_limit_reset - datetime.now()
                await asyncio.sleep(wait_time.total_seconds())
                continue
            except Exception as e:
                print(f'{datetime.now()} - Ocorreu um erro: {e}')
                break

            if not self.tweets:
                print(f'{datetime.now()} - Nenhum tweet encontrado')
                break

            for tweet in self.tweets:
                self.tweet_count += 1
                tweet_data = {
                    'Tweet_count': self.tweet_count,
                    'Username': tweet.user.name,
                    'Text': tweet.text,
                    'Created_At': tweet.created_at,
                    'Retweets': tweet.retweet_count,
                    'Likes': tweet.favorite_count
                }

                # Salvar tweet em CSV
                with open('data/tweets.csv', 'a', newline='', encoding='utf-8') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow([
                        tweet_data['Tweet_count'],
                        tweet_data['Username'],
                        tweet_data['Text'],
                        tweet_data['Created_At'],
                        tweet_data['Retweets'],
                        tweet_data['Likes']
                    ])

                # Adicionar tweet aos dados JSON
                json_data.append(tweet_data)

            print(f'{datetime.now()} - Obtidos {self.tweet_count} tweets')

        # Salvar dados em JSON
        with open('data/tweets.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        print(f'{datetime.now()} - Concluído! Obtidos {self.tweet_count} tweets')
