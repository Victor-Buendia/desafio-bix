def models_to_dict_list(models):
	"""
	Converte uma lista de modelos em uma lista de dicionários.

	Argumentos:
		models (list): Uma lista de objetos modelo a serem convertidos.

	Retorna:
		list: Uma lista de dicionários representando os modelos.
	"""
	data = [model_to_dict(model) for model in models]
	return data

def model_to_dict(model):
	"""
	Converte um objeto model em um dicionário.

	Argumentos:
		model: Um modelo a ser convertido.

	Retorna:
		dict: Um dicionário representando o objeto modelo.
	"""
	return {column.name: getattr(model,column.name) for column in model.__table__.columns}