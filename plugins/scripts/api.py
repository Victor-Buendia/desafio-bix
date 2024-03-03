import requests
import pandas as pd
import io
import os

def retrieve_employees():
	employees = []
	for i in range(1,10):
		payload = {'id':i}
		try:
			result = requests.get(os.environ.get('BIX_ENDPOINT_FUNCIONARIOS'), params=payload)
			employees.append({'id_funcionario': i, 'nome': result.text})

		except Exception as e:
			print(e)
	return employees

def retrieve_categories():
	categories = []
	try:
		result = requests.get(os.environ.get('BIX_ENDPOINT_CATEGORIAS'))
		result.raise_for_status()
		df = pd.read_parquet(io.BytesIO(result.content))
		for index, row in df.iterrows():
			categories.append(
				{'id':row.id,'nome_categoria':row.nome_categoria}
			)
		return categories
	except Exception as e:
		print(e)