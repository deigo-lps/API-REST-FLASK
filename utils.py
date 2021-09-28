from models import Pessoas,Usuarios

def insere_pessoas(nome,idade):
  pessoa=Pessoas(nome=nome,idade=idade)
  pessoa.save()
  #db_session.add(pessoa)
  #db_session.commit()
def consulta_pessoa(nome):
  #pessoas=Pessoas.query.all()
  pessoa=Pessoas.query.filter_by(nome=nome).first()
  return pessoa

"""def altera_pessoa(nome,novo_nome,nova_idade):
  pessoa=Pessoas.query.filter_by(nome=nome).first()
  if novo_nome:
    pessoa.nome=novo_nome
  if nova_idade:
    pessoa.nome=novo_nome
  pessoa.save()
  return pessoa
"""
def exclui_pessoa(nome):
  pessoa=Pessoas.query.filter_by(nome=nome).first()
  pessoa.delete()

def insere_usuario(login,password):
  usuario=Usuarios(login=login,password=password)
  usuario.save()

def consulta_usuarios():
  usuarios=Usuarios.query.all()
  print(usuarios)

if __name__ == '__main__':
  #insere_pessoas()
  #altera_pessoa()
  #exclui_pessoa()
  #consulta_pessoas()
  #insere_usuario('deigo','123')
  #insere_usuario('admin','admin123')
  consulta_usuarios()
