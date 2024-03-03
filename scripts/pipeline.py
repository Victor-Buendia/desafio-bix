import os
import io
import pandas as pd

from connector import DbConnector, Base
from api import ApiIngestor
from inserter import Inserter
from helper import models_to_dict_list

from models.venda import Venda
from models.funcionario import Funcionario
from models.categoria import Categoria

class Main():
	def __init__(self):
		self.api_ingestor = ApiIngestor()
		self.inserter = Inserter()

	def start(self):
		local_psql = DbConnector(
			user='bix',
			pswd='tech',
			host=os.environ.get('DOCKER_DB_HOST', default='localhost'),
			port=os.environ.get('DOCKER_DB_PORT', default=5500),
			db='vendas'
		)
		local_psql.create_tables()

		bix_psql = DbConnector(
			host=os.environ.get('BIX_DB_HOST'),
			port=os.environ.get('BIX_DB_PORT'),
			user=os.environ.get('BIX_DB_USER'),
			pswd=os.environ.get('BIX_DB_PASS'),
			db=os.environ.get('BIX_DB_NAME')
		)

		self.ingest_psql_data(db_from=bix_psql,db_to=local_psql,Table=Venda,pk=Venda.id_venda)
		self.ingest_api_data(db_to=local_psql,Table=Funcionario,pk=Funcionario.id_funcionario)
		self.ingest_parquet_data(db_to=local_psql,Table=Categoria,pk=Categoria.id)

		local_psql.session.close()
		bix_psql.session.close()

	# Categorias
	def ingest_parquet_data(self,db_to,Table,pk):
		result = self.api_ingestor.ingest_from_api(
			api_url=os.environ.get('BIX_ENDPOINT_CATEGORIAS')
		)
		categorias = pd.read_parquet(io.BytesIO(result.content))
		categorias = categorias.to_dict('records')
		self.inserter.insert_data_into_psql(
			Table=Table,
			database=db_to,
			source_data=categorias,
			primary_key=pk
		)

	# Funcionarios
	def ingest_api_data(self,db_to,Table,pk):
		funcionarios = [
			{
				'id_funcionario': id_funcionario,
				'nome': self.api_ingestor.ingest_from_api(
					api_url=os.environ.get('BIX_ENDPOINT_FUNCIONARIOS'),
					payload={'id': id_funcionario}
				).text
			} for id_funcionario in range(1,10)
		]
		self.inserter.insert_data_into_psql(
			Table=Table,
			database=db_to,
			source_data=funcionarios,
			primary_key=pk
		)

	# Vendedores
	def ingest_psql_data(self,db_from,db_to,Table,pk):
		vendas = self.api_ingestor.ingest_from_psql(database=db_from,Table=Table)
		vendas = models_to_dict_list(vendas)
		self.inserter.insert_data_into_psql(
			Table=Table,
			database=db_to,
			source_data=vendas,
			primary_key=pk
		)

main = Main()
main.start()