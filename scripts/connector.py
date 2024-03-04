import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DbConnector():
    """
    Conecta-se a um banco de dados PostgreSQL e fornece métodos para interagir com ele.

    Argumentos:
        user (str): Nome de usuário para acessar o banco de dados.
        pswd (str): Senha para acessar o banco de dados.
        host (str): Endereço do host onde o banco de dados está hospedado.
        port (int): Porta para se conectar ao banco de dados.
        db (str): Nome do banco de dados.

    Atributos:
        __connection_string (str): String de conexão ao banco de dados.
        __engine (objeto Engine): Objeto de mecanismo SQLAlchemy para interagir com o banco de dados.
        __address (str): Endereço do banco de dados no formato 'user@host:port/db'.
        session (objeto Session): Sessão SQLAlchemy para realizar operações no banco de dados.

    Métodos:
        create_tables(): Cria todas as tabelas definidas no modelo.
        get_address(): Retorna o endereço do banco de dados.
    """
    def __init__(self,user,pswd,host,port,db):
        self.__connection_string='postgresql+psycopg2://{user}:{pswd}@{host}:{port}/{db}'.format(
            user=user,
            pswd=pswd,
            host=host,
            port=port,
            db=db
        )
        self.__engine = sqlalchemy.create_engine(self.__connection_string, echo=True)
        self.__address = '{user}@{host}:{port}/{db}'.format(
            user=user,
            host=host,
            port=port,
            db=db
        )
    
        Session = sessionmaker(bind=self.__engine)
        self.session = Session()

    def create_tables(self):
        """
        Cria todas as tabelas definidas no modelo no banco de dados.
        """
        Base.metadata.create_all(self.__engine)

    @property
    def get_address(self):
        """
        Retorna o endereço do banco de dados.
        """
        return self.__address