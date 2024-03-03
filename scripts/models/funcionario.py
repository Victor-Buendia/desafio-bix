from sqlalchemy import Column, Integer, String, Date
from connector import Base

class Funcionario(Base):
	__tablename__ = 'funcionarios'
	__table_args__ = {'extend_existing': True}
	
	id_funcionario = Column(Integer, primary_key=True)
	nome = Column(String)

	def __init__(self, id_funcionario, nome):
		self.id_funcionario = id_funcionario
		self.nome = nome