from sqlalchemy import text
import requests
import os

class ApiIngestor():
	def __init__(self, logger):
		self.logger = logger

	def ingest_from_psql(self,database,Table):
		data = database.session.query(Table).all()
		self.logger.info('DATA SUCCESSFULLY RETRIEVED FROM TABLE {table} LOCATED AT {db_addr}'.format(
			table=Table.__tablename__.upper(),
			db_addr=database.get_address
		))
		return data

	def ingest_from_api(self,api_url,payload={}):
		try:
			result = requests.get(api_url, params=payload)
			self.logger.info('API REQUEST SUCCESSFULLY RETURNED DATA')
			return result
		except Exception as e:
			print(e)