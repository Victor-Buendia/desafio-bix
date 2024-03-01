from sqlalchemy import Column, Integer, String, Date
from connector import Base

class Categoria(Base):
	__tablename__ = 'categorias'

	id = Column(Integer, primary_key=True)
	nome_categoria = Column(String)

	def __init__(self, id, nome_categoria):
		self.id = id
		self.nome_categoria = nome_categoria