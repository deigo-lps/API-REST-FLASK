from sqlalchemy import create_engine,Column,Integer,String,ForeignKey
from sqlalchemy.orm import scoped_session,sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base

engine=create_engine('sqlite:///atividades.db',connect_args={'check_same_thread': False},
convert_unicode=True)#pra acento
db_session=scoped_session(sessionmaker(autocommit=False,bind=engine))

Base=declarative_base()
Base.query=db_session.query_property()

#-------------------------------------------------------------------------#

class Pessoas(Base):
  __tablename__='pessoas'
  id=Column(Integer,primary_key=True)
  nome=Column(String(40),index=True)
  idade=Column(Integer)

  #quando mandar imprimir objeto vai imprimir oq tiver nessa função.
  #representation
  def __repr__(self):
    return'<Pessoa ID:{} Nome:{}>'.format(self.id,self.nome)

  def save(self):
    db_session.add(self)
    db_session.commit()

  def delete(self):
    db_session.delete(self)
    db_session.commit()

class Atividades(Base):
  __tablename__='atividades'
  id=Column(Integer,primary_key=True)
  nome=Column(String(80))
  status=Column(String(20))
  pessoa_id=Column(Integer,ForeignKey('pessoas.id'))
  pessoa=relationship("Pessoas")

  def __repr__(self):
    return'<Atividades {}>'.format(self.nome)

  def save(self):
    db_session.add(self)
    db_session.commit()

  def delete(self):
    db_session.delete(self)
    db_session.commit()

class Usuarios(Base):
  __tablename__='usuarios'
  id=Column(Integer,primary_key=True)
  login=Column(String(20),unique=True)
  password=Column(String(20))

  def __repr__(self):
    return '<Usuario id:{} login:{}>'.format(self.id,self.login)

  def save(self):
    db_session.add(self)
    db_session.commit()

  def delete(self):
    db_session.delete(self)
    db_session.commit()

#cria o banco de dados
def init_db():
  Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
  init_db()
