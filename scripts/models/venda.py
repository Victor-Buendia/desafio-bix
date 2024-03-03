from sqlalchemy import Column, Integer, String, Date
from connector import Base

class Venda(Base):
	__tablename__ = 'venda'
	__table_args__ = {'extend_existing': True}
	
	id_venda = Column(Integer, primary_key=True)
	id_funcionario = Column(Integer)
	id_categoria = Column(Integer)
	data_venda = Column(Date)
	venda = Column(Integer)
	

	def __init__(self, id_venda, id_funcionario, id_categoria, data_venda, venda):
		self.id_venda = id_venda
		self.id_funcionario = id_funcionario
		self.id_categoria = id_categoria
		self.data_venda = data_venda
		self.venda = venda