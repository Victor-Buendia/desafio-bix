from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, OperationalError
import os

from connector import DbConnector, Base
from api import retrieve_employees, retrieve_categories

from models.venda import Venda
from models.funcionario import Funcionario
from models.categoria import Categoria

def main():
	local_psql = DbConnector(user='bix',pswd='tech',host='banco',port='5432',db='vendas')
	bix_psql = DbConnector(
		host=os.environ.get('BIX_DB_HOST'),
		port=os.environ.get('BIX_DB_PORT'),
		user=os.environ.get('BIX_DB_USER'),
		pswd=os.environ.get('BIX_DB_PASS'),
		db=os.environ.get('BIX_DB_NAME')
	)

	local_psql.create_tables()

	source_data = bix_psql.session.execute(text("SELECT * FROM public.venda"))
	loaded_data = [row.id_venda for row in local_psql.session.execute(text("SELECT id_venda FROM vendas"))]

	vendas = []
	funcionarios = []
	categorias = []

	for row in source_data:
		if row.id_venda not in loaded_data: # Prevent duplicate insertion
			vendas.append(
				Venda(
					id_venda=row.id_venda,
					id_funcionario=row.id_funcionario,
					id_categoria=row.id_categoria,
					data_venda=row.data_venda,
					venda=row.venda
				)
			)
	try:
		if vendas != []:
			local_psql.session.add_all(vendas)
			local_psql.session.commit()
	except (IntegrityError, OperationalError) as e:
				print(f"Error: {e}")

	loaded_employees = [row.id_funcionario for row in local_psql.session.execute(text("SELECT id_funcionario FROM funcionarios"))]
	for row in retrieve_employees():
		if row['id_funcionario'] not in loaded_employees:
			funcionarios.append(
				Funcionario(
					id_funcionario=row['id_funcionario'],
					nome=row['nome']
				)
			)
	try:
		if funcionarios != []:
			local_psql.session.add_all(funcionarios)
			local_psql.session.commit()
	except (IntegrityError, OperationalError) as e:
				print(f"Error: {e}")

	loaded_categories = [row.id for row in local_psql.session.execute(text("SELECT id FROM categorias"))]
	for row in retrieve_categories():
		if row['id'] not in loaded_categories:
			categorias.append(
				Categoria(
					id=row['id'],
					nome_categoria=row['nome_categoria']
				)
			)

	try:
		if categorias != []:
			local_psql.session.add_all(categorias)
			local_psql.session.commit()
	except (IntegrityError, OperationalError) as e:
				print(f"Error: {e}")

	local_psql.session.close()
	bix_psql.session.close()