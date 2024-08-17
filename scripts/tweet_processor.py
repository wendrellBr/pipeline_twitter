import pandas as pd
from nltk.corpus import stopwords

class TweetProcessor:
    """
    Classe responsável por processar e limpar os dados dos tweets.
    """

    def __init__(self, file_path):
        """
        Inicializa o processador de tweets com o caminho do arquivo CSV.

        :param file_path: Caminho para o arquivo CSV com os tweets.
        """
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """
        Carrega os dados do CSV em um DataFrame.
        """
        self.df = pd.read_csv(self.file_path, encoding='utf-8')

    def clean_data(self):
        """
        Realiza a limpeza e transformação dos dados.
        """
        # Remover URLs da coluna 'Text'
        self.df['Text'] = self.df['Text'].str.replace(r'http\S+', '', regex=True)

        # Converter a coluna 'Created_At' para o formato de data, removendo o fuso horário
        self.df['Created_At'] = pd.to_datetime(self.df['Created_At']).dt.strftime('%Y-%m-%d %H:%M:%S')

        # Criar uma coluna de comprimento do tweet
        self.df['Tweet_Length'] = self.df['Text'].str.len()

        # Remover stopwords
        stop_words = set(stopwords.words('portuguese'))
        self.df['Text'] = self.df['Text'].apply(lambda x: ' '.join(word for word in x.split() if word not in stop_words))

        # Contar hashtags e menções
        self.df['Hashtag_Count'] = self.df['Text'].str.count('#')
        self.df['Mention_Count'] = self.df['Text'].str.count('@')

    def get_data(self):
        """
        Retorna o DataFrame processado.

        :return: DataFrame com os dados processados.
        """
        return self.df
