from sqlalchemy import text
import requests
import os


class ApiIngestor():
	def __init__(self):
		pass

	def ingest_from_psql(self,database,Table):
		return database.session.query(Table).all()

	def ingest_from_api(self,api_url,payload={}):
		try:
			result = requests.get(api_url, params=payload)
			return result
		except Exception as e:
			print(e)