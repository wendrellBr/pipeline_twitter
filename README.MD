# TwitterPipeline

Este projeto é uma solução simples para coletar, processar e armazenar tweets no MongoDB. Ele utiliza a lib do twikit para obter tweets com base em uma consulta específica, processa os dados e os insere em um banco de dados MongoDB.

## Descrição

O pipeline é dividido em três etapas principais:

1. **Coleta de Tweets**: Usa a lib do Twikit para buscar tweets no Twitter que atendem a critérios específicos.
2. **Processamento de Dados**: Limpa e transforma os dados dos tweets.
3. **Armazenamento em MongoDB**: Insere os dados processados em uma coleção do MongoDB.

## Pré-Requisitos

Certifique-se de ter os seguintes itens instalados:

- Python 3.8 ou superior
- Bibliotecas Python necessárias (listadas abaixo)
- Conta no Twitter
- MongoDB configurado e em execução

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   cd SEU_REPOSITORIO
   ```

2. **Crie um ambiente virtual e ative-o:**

   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**

   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

   ```env
   NAME=seu_nome_de_usuario
   EMAIL=seu_email
   PASSWORD=sua_senha
   MONGO_URI=sua_uri_do_mongodb
   ```

   **Nota:** A URI do MongoDB deve seguir o formato `mongodb+srv://<usuario>:<senha>@<cluster>/<db>?retryWrites=true&w=majority`.

## Estrutura do Projeto

- **`twitter_client.py`**: Contém a classe `TwitterClient` responsável por coletar tweets.
- **`tweet_processor.py`**: Contém a classe `TweetProcessor` responsável por limpar e transformar os dados dos tweets.
- **`mongo_handler.py`**: Contém a classe `MongoHandler` responsável por interagir com o MongoDB.
- **`main.py`**: Script principal que integra todas as etapas do pipeline.

## Uso

Para executar o pipeline e coletar, processar e armazenar os tweets, execute o seguinte comando:

```bash
python main.py
```

### Configuração do `main.py`

- **Parâmetros da Consulta**: No arquivo `main.py`, você pode ajustar a consulta (`query`) e o número mínimo de tweets (`min_tweets`) para personalizar a busca de tweets.

## Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE).
