def models_to_dict_list(models):
	data = [model_to_dict(model) for model in models]
	return data

def model_to_dict(model):
	return {column.name: getattr(model,column.name) for column in model.__table__.columns}

def parquet_to_dict(parquet):
	return 