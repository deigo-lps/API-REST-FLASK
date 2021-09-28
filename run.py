from flask import Flask,request
from flask_restful import Resource,Api
from models import Pessoas,Atividades,Usuarios
from flask_httpauth import HTTPBasicAuth

app=Flask(__name__)
api=Api(app)
auth=HTTPBasicAuth()

#USUARIOS={'deigo':'123','admin':'admin123'}

#@auth.verify_password
#def verificacao(login,password):
#  if not (login,password):
#    return False
#  return USUARIOS.get(login)==password

@auth.verify_password
def verificacao(login,password):
  if not (login,password):
    return False
  return Usuarios.query.filter_by(login=login,password=password).first()


class Pessoa(Resource):
  def get(self,nome):
    pessoa=Pessoas.query.filter_by(nome=nome).first()
    try:
      response={'id':pessoa.id,'nome':pessoa.nome,'idade':pessoa.idade}
    except AttributeError:
      return {'message':'pessoa não existente.'}
    return response

  @auth.login_required
  def put(self,nome):
    pessoa=Pessoas.query.filter_by(nome=nome).first()
    if pessoa is not None:
      dados=request.json
      if 'nome' in dados:
        pessoa.nome=dados['nome']
      if 'idade' in dados:
        pessoa.idade=dados['idade']
      pessoa.save()
      return {'id':pessoa.id,'nome':pessoa.nome,'idade':pessoa.idade}
    else:
      return {'message':'pessoa não existente.'}

  @auth.login_required
  def delete(self,nome):
    pessoa=Pessoas.query.filter_by(nome=nome).first()
    if pessoa is not None:
      pessoa.delete()
      return {'status':'sucesso'}
    else:
      return {'message':'pessoa não existente.'}

class ListaPessoas(Resource):
  def get(self):
    pessoas=Pessoas.query.all()
    response=[{'id':i.id,'nome':i.nome,'idade':i.idade} for i in pessoas]
    return response

  @auth.login_required
  def post(self):
    dados=request.json
    pessoa=Pessoas(nome=dados['nome'],idade=dados['idade'])
    pessoa.save()
    return {'id':pessoa.id,'nome':pessoa.nome,'idade':pessoa.idade}

class ListaAtividades(Resource):
  @auth.login_required
  def post(self):
    dados=request.json
    pessoa=Pessoas.query.filter_by(nome=dados['pessoa']).first()
    if pessoa is not None:
      atividade=Atividades(nome=dados['nome'],pessoa=pessoa,status=dados['status'])
      atividade.save()
      response={'id':atividade.id,'pessoa_id':atividade.pessoa_id,'pessoa':atividade.pessoa.nome,'nome':atividade.nome,'status':atividade.status}
      return response
    else:
      return{'message':'pessoa não existente.'}
  def get(self):
    atividades=Atividades.query.all()
    response=[{'id':i.id,'pessoa_id':i.pessoa_id,'pessoa':i.pessoa.nome,'nome':i.nome,'status':i.status} for i in atividades]
    return response

class ListaAtPes(Resource):
  def get(self,nome):
    pessoa=Pessoas.query.filter_by(nome=nome).first()
    atividades=Atividades.query.filter_by(pessoa=pessoa)
    if atividades is not None:
      response=[{'id':i.id,'pessoa_id':i.pessoa_id,'pessoa':i.pessoa.nome,'nome':i.nome,'status':i.status} for i in atividades]
      return response
    else:
      return{'message':'Atividades não encontradas.'}

class AtividadeID(Resource):
  @auth.login_required
  def put(self,id):
    try:
      dados=request.json['status']
    except TypeError:
      return{'message':'status não encontrado no body'}
    atividade=Atividades.query.filter_by(id=id).first()
    if atividade is not None:
      atividade.status=dados
      atividade.save()
      return {'id':atividade.id,'pessoa_id':atividade.pessoa_id,'pessoa':atividade.pessoa.nome,'nome':atividade.nome,'status':atividade.status}
    else:
      return{'message':'Atividade não encontrada.'}

  @auth.login_required
  def delete(self,id):
    atividade=Atividades.query.filter_by(id=id).first()
    if atividade is not None:
      atividade.delete()
      return{'oss':'oss'}
    else:
      return{'message':'atividade não encontrada.'}


api.add_resource(Pessoa,'/pessoa/<string:nome>/')
api.add_resource(ListaPessoas,'/pessoa/')
api.add_resource(ListaAtividades,'/atividades/')
api.add_resource(ListaAtPes,'/atividades/<string:nome>/')
api.add_resource(AtividadeID,'/atividades/<int:id>/')
if __name__ == '__main__':
  app.run(debug=True)
