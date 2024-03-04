from sqlalchemy import text
import requests
import os

class ApiIngestor():
	"""
    Realiza a ingestão de dados a partir de uma tabela PostgreSQL ou de uma API.

    Argumentos:
        logger: Um objeto logger para registrar os logs.

    Métodos:
        ingest_from_psql(database, Table): Coleta dados de uma tabela PostgreSQL.
        ingest_from_api(api_url, payload={}): Coleta dados de uma API por meio de uma requisição.
    """
	def __init__(self, logger):
		self.logger = logger

	def ingest_from_psql(self,database,Table):
		"""
		Coleta dados de uma tabela PostgreSQL.

		Argumentos:
			database (objeto): Uma instância de DbConnector.
			Table (classe): A classe modelo representando a tabela do banco de dados.

		Retorna:
			list: Uma lista contendo os dados recuperados da tabela.
		"""
		data = database.session.query(Table).all()
		self.logger.info('DATA SUCCESSFULLY RETRIEVED FROM TABLE {table} LOCATED AT {db_addr}'.format(
			table=Table.__tablename__.upper(),
			db_addr=database.get_address
		))
		return data

	def ingest_from_api(self,api_url,payload={}):
		"""
		Coleta dados de uma API por meio de uma requisição.

		Argumentos:
			api_url (str): A URL da API de onde os dados serão coletados.
			payload (dict): Parâmetros opcionais para a solicitação GET (padrão: {}).

		Retorna:
			objeto Response: O resultado da solicitação GET.

		Exceções:
			Exception: Se ocorrer um erro durante a solicitação.
		"""
		try:
			result = requests.get(api_url, params=payload)
			self.logger.info('API REQUEST SUCCESSFULLY RETURNED DATA')
			return result
		except Exception as e:
			print(e)