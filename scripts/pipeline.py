import os
import io
import logging

import pandas as pd

from api import ApiIngestor
from inserter import Inserter
from connector import DbConnector, Base
from helper import models_to_dict_list
from validator import VendasList, VendaValidator, FuncionariosList, FuncionarioValidator, CategoriasList, CategoriaValidator
from environment import Environment

from models.venda import Venda
from models.funcionario import Funcionario
from models.categoria import Categoria

class Main():
	def __init__(self):
		self.env = Environment()
		self.logger = logging.getLogger(__name__)
		self.api_ingestor = ApiIngestor(self.logger)
		self.inserter = Inserter(self.logger)
		self.logger.debug(f"ATTEMPTING TO CONNECT TO DATABASE bix:tech@{self.env.load_env('DOCKER_DB_HOST', default='localhost')}:{self.env.load_env('DOCKER_DB_PORT', default=5500)}/vendas")
		self.local_psql = self.start(
			user='bix',
			pswd='tech',
			host=self.env.load_env('DOCKER_DB_HOST', default='localhost'),
			port=self.env.load_env('DOCKER_DB_PORT', default=5500),
			db='vendas'
		)
		self.logger.info(f"SUCCESSFULLY CONNECTED TO DATABASE {self.local_psql.get_address}")

	def start(self,user,pswd,host,port,db):
		"""
        Inicia a conexão com o banco de dados.

        Argumentos:
            user (str): Nome de usuário para acessar o banco de dados.
            pswd (str): Senha para acessar o banco de dados.
            host (str): Endereço do host onde o banco de dados está hospedado.
            port (int): Porta para se conectar ao banco de dados.
            db (str): Nome do banco de dados.

        Retorna:
            objeto DbConnector: A conexão ao banco de dados.

        Exceções:
            Exception: Se ocorrer um erro durante a conexão.
        """
		try:
			db = DbConnector(user,pswd,host,port,db)
			self.logger.info(f"SUCCESSFULLY CONNECTED TO DATABASE {db.get_address}")
			return db
		except Exception as e:
			self.logger.error(e)

	def close_connection(self,db=None):
		"""
        Fecha a conexão com o banco de dados.

        Argumentos:
            db (objeto, opcional): A conexão ao banco de dados a ser fechada. Se não especificado, fecha a conexão local.
        """
		db = self.local_psql if db == None else db
		try:
			db.session.close()
			self.logger.info(f"DISCONNECTED FROM DATABASE {db.get_address}")
		except Exception as e:
			self.logger.error(e)
		
	# Categorias
	def ingest_categorias(self,db_to):
		"""
        Ingestão de dados de categorias.

        Argumentos:
            db_to (objeto): A conexão ao banco de dados de destino.
        """
		categorias = self.ingest_parquet_data(db_to=self.local_psql,Table=Categoria,pk=Categoria.id)
		categorias = CategoriasList.parse_obj(categorias) # Validation
		self.logger.info('DATA FROM CATEGORIAS SUCCESSFULLY VALIDATED WITH PYDANTIC')
		self.inserter.insert_data_into_psql(
			Table=Categoria,
			database=db_to,
			source_data=categorias.model_dump(),
			primary_key=Categoria.id
		)
	def ingest_parquet_data(self,db_to,Table,pk):
		"""
        Ingestão de dados de um arquivo Parquet.

        Argumentos:
            db_to (objeto): A conexão ao banco de dados de destino.
            Table (classe): A classe modelo representando a tabela do banco de dados.
            pk (str): O nome da chave primária.

        Retorna:
            list: Uma lista contendo os dados recuperados do arquivo Parquet.
        """
		result = self.api_ingestor.ingest_from_api(
			api_url=self.env.load_env('BIX_ENDPOINT_CATEGORIAS')
		)
		categorias = pd.read_parquet(io.BytesIO(result.content))
		categorias = categorias.to_dict('records')
		return categorias

	# Funcionarios
	def ingest_funcionarios(self,db_to):
		"""
        Ingestão de dados de funcionários.

        Argumentos:
            db_to (objeto): A conexão ao banco de dados de destino.
        """
		funcionarios = self.ingest_api_data(db_to=db_to,Table=Funcionario,pk=Funcionario.id_funcionario)
		funcionarios = FuncionariosList.parse_obj(funcionarios) # Validation
		self.logger.info('DATA FROM FUNCIONARIOS SUCCESSFULLY VALIDATED WITH PYDANTIC')
		self.inserter.insert_data_into_psql(
			Table=Funcionario,
			database=db_to,
			source_data=funcionarios.model_dump(),
			primary_key=Funcionario.id_funcionario
		)
	def ingest_api_data(self,db_to,Table,pk):
		"""
        Ingestão de dados de uma API.

        Argumentos:
            db_to (objeto): A conexão ao banco de dados de destino.
            Table (classe): A classe modelo representando a tabela do banco de dados.
            pk (str): O nome da chave primária.

        Retorna:
            list: Uma lista contendo os dados recuperados da API.
        """
		funcionarios = [
			{
				'id_funcionario': id_funcionario,
				'nome': self.api_ingestor.ingest_from_api(
					api_url=self.env.load_env('BIX_ENDPOINT_FUNCIONARIOS'),
					payload={'id': id_funcionario}
				).text
			} for id_funcionario in range(1,10)
		]
		return funcionarios

	# Vendedores
	def ingest_vendas(self,db_from,db_to):
		"""
        Ingestão de dados de vendas.

        Argumentos:
            db_from (objeto): A conexão ao banco de dados de origem.
            db_to (objeto): A conexão ao banco de dados de destino.
        """
		vendas = self.ingest_psql_data(db_from=db_from,db_to=db_to,Table=Venda,pk=Venda.id_venda)
		vendas = VendasList.parse_obj(vendas) # Validation
		self.logger.info('DATA FROM VENDAS SUCCESSFULLY VALIDATED WITH PYDANTIC')
		self.inserter.insert_data_into_psql(
			Table=Venda,
			database=db_to,
			source_data=vendas.model_dump(),
			primary_key=Venda.id_venda
		)
	def ingest_psql_data(self,db_from,db_to,Table,pk):
		"""
        Ingestão de dados do banco de dados PostgreSQL.

        Argumentos:
            db_from (objeto): A conexão DbConnector ao banco de dados de origem.
            db_to (objeto): A conexão DbConnector ao banco de dados de destino.
            Table (classe): A classe modelo representando a tabela do banco de dados.
            pk (str): O nome da chave primária.

        Retorna:
            list: Uma lista contendo os dados recuperados do banco de dados PostgreSQL.
        """
		vendas = self.api_ingestor.ingest_from_psql(database=db_from,Table=Table)
		vendas = models_to_dict_list(vendas)
		return vendas

if __name__ == '__main__':
	main = Main()