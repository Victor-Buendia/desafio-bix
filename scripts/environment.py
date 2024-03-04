import os
import logging

class Environment():
	"""
    Gerencia as variáveis de ambiente necessárias para a aplicação.

    Métodos:
        check_env_variables(): Verifica se todas as variáveis de ambiente necessárias foram definidas.
        retrieve_env_variables(): Recupera as variáveis de ambiente necessárias.
        load_env(env_name): Carrega uma variável de ambiente.

    Atributos:
        logger: Um objeto de registro para mensagens de log.
        missing_variables: Uma lista de variáveis de ambiente ausentes.
    """
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.missing_variables = list()
	
	class MissingEnvVariablesException(Exception):
		"""
        Exceção lançada quando as variáveis de ambiente necessárias estão ausentes.
        """
		def __init__(self,env_name,environment):
			message = f"Pipeline configuration failed because you have the following environment valuables missing in you .env file:"
			environment.logger.error(message)
			environment.logger.error('\n'.join(map(str,env_name)))

	def check_env_variables(self):
		"""
        Verifica se todas as variáveis de ambiente necessárias foram definidas.

        Exceções:
            MissingEnvVariablesException: Se alguma variável de ambiente estiver ausente.
        """
		if self.missing_variables != []:
			raise self.MissingEnvVariablesException(self.missing_variables,self)
		else:
			self.logger.info(f"ALL ENVIRONMENT VARIABLES WERE SUCCESSFULLY LOADED")

	def retrieve_env_variables(self):
		"""
        Recupera e atribui as variáveis de ambiente necessárias.
        """
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
		"""
        Carrega uma variável de ambiente específica.

        Argumentos:
            env_name (str): Nome da variável de ambiente a ser carregada.

        Retorna:
            str: O valor da variável de ambiente carregada, se existir.
        """
		variable = os.environ.get(env_name)
		if variable == "":
			self.missing_variables.append(env_name)
		else:
			return variable