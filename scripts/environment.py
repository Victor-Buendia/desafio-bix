import os
import logging

class Environment():
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.missing_variables = list()
	
	class MissingEnvVariablesException(Exception):
		def __init__(self,env_name):
			message = f"Pipeline configuration failed because you have the following environment valuables missing in you .env file:"
			self.logger.error(message)
			self.logger.error('\n'.join(map(str,self.missing_variables)))

	def check_env_variables(self):
		if self.missing_variables != []:
			raise MissingEnvVariablesException(self.missing_variables)
		else:
			self.logger.info(f"ALL ENVIRONMENT VARIABLES WERE SUCCESSFULLY LOADED")

	def retrieve_env_variables(self):
		self.BIX_DB_HOST=self.load_env('BIX_DB_HOST')
		self.BIX_DB_PORT=self.load_env('BIX_DB_PORT')
		self.BIX_DB_USER=self.load_env('BIX_DB_USER')
		self.BIX_DB_PASS=self.load_env('BIX_DB_PASS')
		self.BIX_DB_NAME=self.load_env('BIX_DB_NAME')
		self.BIX_ENDPOINT_FUNCIONARIOS=self.load_env('BIX_ENDPOINT_FUNCIONARIOS')
		self.BIX_ENDPOINT_CATEGORIAS=self.load_env('BIX_ENDPOINT_CATEGORIAS')
		self.DOCKER_DB_HOST=self.load_env('DOCKER_DB_HOST')
		self.DOCKER_DB_PORT=self.load_env('DOCKER_DB_PORT')

	def load_env(self,env_name):
		variable = os.environ.get(env_name)
		if variable == "":
			self.missing_variables.append(env_name)
		else:
			return variable