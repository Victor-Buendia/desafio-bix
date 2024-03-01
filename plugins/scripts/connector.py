import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DbConnector():
    def __init__(self,user,pswd,host,port,db):
        self.__connection_string='postgresql+psycopg2://{user}:{pswd}@{host}:{port}/{db}'.format(
            user=user,
            pswd=pswd,
            host=host,
            port=port,
            db=db
        )
        self.__engine = sqlalchemy.create_engine(self.__connection_string, echo=False)
    
        Session = sessionmaker(bind=self.__engine)
        self.session = Session()

    def create_tables(self):
        Base.metadata.create_all(self.__engine)