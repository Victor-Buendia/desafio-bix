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
		self.local_psql = self.start(
			user='bix',
			pswd='tech',
			host=os.environ.get('DOCKER_DB_HOST', default='localhost'),
			port=os.environ.get('DOCKER_DB_PORT', default=5500),
			db='vendas'
		)

	def start(self,user,pswd,host,port,db):
		db = DbConnector(user,pswd,host,port,db)
		return db

	def close_connection(self,db=None):
		db = self.local_psql if db == None else db
		db.session.close()
		
	# Categorias
	def ingest_categorias(self,db_to):
		self.ingest_parquet_data(db_to=self.local_psql,Table=Categoria,pk=Categoria.id)
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
	def ingest_funcionarios(self,db_to):
		self.ingest_api_data(db_to=db_to,Table=Funcionario,pk=Funcionario.id_funcionario)
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
	def ingest_vendas(self,db_from,db_to):
		self.ingest_psql_data(db_from=db_from,db_to=db_to,Table=Venda,pk=Venda.id_venda)
	def ingest_psql_data(self,db_from,db_to,Table,pk):
		vendas = self.api_ingestor.ingest_from_psql(database=db_from,Table=Table)
		vendas = models_to_dict_list(vendas)
		self.inserter.insert_data_into_psql(
			Table=Table,
			database=db_to,
			source_data=vendas,
			primary_key=pk
		)

if __name__ == '__main__':
	main = Main()