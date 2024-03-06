from pydantic import BaseModel, validator, PositiveInt, RootModel
from typing import List

from datetime import date

from api import ApiIngestor
from models.venda import Venda as VendaModel
from helper import models_to_dict_list

class VendaValidator(BaseModel):
	id_venda: PositiveInt
	id_funcionario: PositiveInt
	id_categoria: PositiveInt
	data_venda: date
	venda: PositiveInt

class VendasList(RootModel):
	root: List[VendaValidator]

class FuncionarioValidator(BaseModel):
	id_funcionario: PositiveInt
	nome: str

class FuncionariosList(RootModel):
	root: List[FuncionarioValidator]

class CategoriaValidator(BaseModel):
	id: PositiveInt
	nome_categoria: str

class CategoriasList(RootModel):
	root: List[CategoriaValidator]