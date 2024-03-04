from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.dialects.sqlite import insert

class Inserter():
	def __init__(self,logger):
		self.logger = logger

	def insert_data_into_psql(self,database,source_data,Table,primary_key):
		"""
		Insere dados em uma tabela PostgreSQL.

		Argumentos:
			database (objeto): Uma instância de DbConnector.
			source_data (dict): Os dados a serem inseridos na tabela.
			Table (classe): A classe modelo representando a tabela do banco de dados.
			primary_key (str): O nome da coluna que serve como chave primária.

		Exceções:
			IntegrityError, OperationalError: Se ocorrer um erro durante a inserção dos dados.
		"""
		data = source_data
		try:
			insert_stmt = insert(Table).values(data)
			insert_stmt = insert_stmt.on_conflict_do_update(
				index_elements=[primary_key],
				set_=dict(insert_stmt.excluded)
			)
			database.session.execute(insert_stmt)
			database.session.commit()
			self.logger.info('DATA SUCCESSFULLY INSERTED IN DATABASE {db_addr} IN TABLE {table}'.format(
				table=Table.__tablename__.upper(),
				db_addr=database.get_address
			))
		except (IntegrityError, OperationalError) as e:
			print(f"Error: {e}")