from threading import local
from flask import Flask, Response, request, sessions
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/projetoimigrante'
db = SQLAlchemy(app)

# INICIANDO A API DOS IMIGRANTES

class usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))
    nacionalidade = db.Column(db.String(50))
    estadoCivil = db.Column(db.String(50))
    endereco = db.Column(db.String(100))
    telefone = db.Column(db.String(14))


    def to_json(self):
        return {"id":self.id, "nome":self.nome, "email":self.email, "nacionalidade":self.nacionalidade, 
         "estadoCivil":self.estadoCivil, "endereco":self.endereco, "telefone":self.telefone
        }


# SELECIONANDO TODOS OS USUÁRIOS

@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuarios_objetos = usuario.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios_objetos]
    print(usuarios_json)

    return gera_response(200, "usuarios", usuarios_json, "ok")

#SELECIONANDO SOMENTE UM USUÁRIO

@app.route("/usuario/<id>", methods=["GET"])
def seleciona_usuario(id):
    usuario_objeto = usuario.query.filter_by(id=id).first()
    usuario_json = usuario_objeto.to_json()

    return gera_response(200, "usuarios", usuario_json)

# CADASTRANDO UM NOVO USUÁRIO

@app.route("/usuario", methods=["POST"])
def cria_usuario():
    body = request.get_json()

    try:
        usuarios = usuario(nome=body["nome"], email=body["email"], nacionalidade=body["nacionalidade"], 
            estadoCivil=body["estadoCivil"], endereco=body["endereco"], telefone=body["telefone"]
        )  # DA LINHA 54 À LINHA 56 ESTÁ SENDO CRIADO UM USUÁRIO 
        db.session.add(usuarios) 
        db.session.commit()
        return gera_response(201, "usuarios", usuarios.to_json(), "Usuário criado com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "usuarios", {}, "Erro ao cadastrar")

# ATUALIZANDO UM USUÁRIO

@app.route("/usuario/<id>", methods=["PUT"])
def atualiza_usuario(id):
    usuario_objeto = usuario.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome' in body):
            usuario_objeto.nome = body['nome']
        if('email' in body):
            usuario_objeto.email = body['email']
        if('nacionalidade' in body):
            usuario_objeto.nacionalidade = body['nacionalidade']
        if('estadoCivil' in body):    
            usuario_objeto.estadoCivil = body['estadoCivil']
        if('endereco' in body):    
            usuario_objeto.endereco = body['endereco']
        if('telefone' in body):    
            usuario_objeto.telefone = body['telefone']

        db.session.add(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuarios", usuario_objeto.to_json(), "Atualizado com sucesso!")
    except Exception as e:
        print(e)
        return gera_response(400, "usuarios", {}, "Erro ao atualizar")

# DELETANDO UM USUÁRIO

@app.route("/usuario/<id>", methods=["DELETE"])
def deleta_usuario(id):
    usuario_objeto = usuario.query.filter_by(id=id).first()

    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuarios", usuario_objeto.to_json(), "Usuário excluído com sucesso!")
    except Exception as e:
        print(e)
        return gera_response(400, "usuarios", {}, "Erro ao excluir")

# INICIANDO API DOS DADOS PROFISSIONAIS DO IMIGRANTE

class experiencia(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa = db.Column(db.String(50))
    cargo = db.Column(db.String(100))
    inicio = db.Column(db.String(50))
    fim = db.Column(db.String(50))
    observacao = db.Column(db.String(100))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    def to_json(self):
        return{
            "id":self.id, "empresa":self.empresa, "cargo":self.cargo, "inicio":self.inicio, 
            "fim":self.fim, "observacao":self.observacao, "usuario_id":self.usuario_id

        }

# SELECIONANDO TODAS AS EXPERIENCIAS

@app.route("/experiencias", methods=["GET"])
def seleciona_experiencias():
    experiencia_objetos = experiencia.query.all()
    experiencia_json = [experiencia.to_json() for experiencia in experiencia_objetos]
    print(experiencia_json)

    return gera_response(200, "experiencia", experiencia_json, "ok")


# SELECIONANDO SOMENTE UMA EXPERIÊNCIA

@app.route("/experiencia/<id>", methods=["GET"])
def seleciona_experiencia(id):
    experiencia_objeto = experiencia.query.filter_by(id=id).first()
    experiencia_json = experiencia_objeto.to_json()

    return gera_response(200, "experiencia", experiencia_json)

# CADASTRANDO UMA NOVA EXPERIÊNCIA

@app.route("/experiencia", methods=["POST"])
def cria_experiencia():
    body = request.get_json()

    try:
        experiencias = experiencia(empresa=body["empresa"], cargo=body["cargo"], inicio=body["inicio"], 
            fim=body["fim"], observacao=body["observacao"], usuario_id=body["usuario_id"]
        )  # DA LINHA 149 À LINHA 150 ESTÁ SENDO CRIADO UM USUÁRIO 
        db.session.add(experiencias) 
        db.session.commit()
        return gera_response(201, "experiencias", experiencias.to_json(), "Uma nova experiência adicionada com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "experiencias", {}, "Erro ao cadastrar")

# ATUALIZANDO UMA EXPERIÊNCIA

@app.route("/experiencia/<id>", methods=["PUT"])
def atualiza_experiencia(id):
    experiencia_objeto = experiencia.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('empresa' in body):
            experiencia_objeto.empresa = body['empresa']
        if('cargo' in body):
            experiencia_objeto.cargo = body['cargo']
        if('inicio' in body):
            experiencia_objeto.inicio = body['inicio']
        if('fim' in body):    
            experiencia_objeto.fim = body['fim']
        if('observacao' in body):    
            experiencia_objeto.observacao = body['observacao']
        if('usuario_id' in body):    
            experiencia_objeto.usuario_id = body['usuario_id']

        db.session.add(experiencia_objeto)
        db.session.commit()
        return gera_response(200, "experiencias", experiencia_objeto.to_json(), "Atualizado com sucesso!")
    except Exception as e:
        print(e)
    return gera_response(400, "experiencias", {}, "Erro ao atualizar")

# DELETANDO UMA EXPERIENCIA 
@app.route("/experiencia/<id>", methods=["DELETE"])
def deleta_experiencia(id):
    experiencia_objeto = experiencia.query.filter_by(id=id).first()

    try:
        db.session.delete(experiencia_objeto)
        db.session.commit()
        return gera_response(200, "experiencias", experiencia_objeto.to_json(), "Experiência excluída com sucesso!")
    except Exception as e:
        print(e)
        return gera_response(400, "experiencias", {}, "Erro ao excluir")

# INICIANDO A API DE VAGAS


class vaga(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cargo = db.Column(db.String(50))
    empresa = db.Column(db.String(100))
    local = db.Column(db.String(50))
    tipoVaga = db.Column(db.String(50))

    def to_json(self):
        return{
            "id":self.id, "cargo":self.cargo, "empresa":self.empresa, 
            "local":self.local, "tipoVaga":self.tipoVaga
        }

# SELECIONANDO TODAS AS VAGAS 

@app.route("/vagas", methods=["GET"])
def seleciona_vagas():
    vaga_objetos = vaga.query.all()
    vaga_json = [vaga.to_json() for vaga in vaga_objetos]
    print(vaga_json)

    return gera_response(200, "vaga", vaga_json, "ok")


# SELECIONANDO SOMENTE UMA VAGA

@app.route("/vaga/<id>", methods=["GET"])
def seleciona_vaga(id):
    vaga_objeto = vaga.query.filter_by(id=id).first()
    vaga_json = vaga_objeto.to_json()

    return gera_response(200, "vaga", vaga_json)


# CADASTRAR UMA NOVA VAGA

@app.route("/vaga", methods=["POST"])
def cria_vaga():
    body = request.get_json()

    try:
        vagas = vaga(cargo=body["cargo"], empresa=body["empresa"], local=body["local"], 
            tipoVaga=body["tipoVaga"],
        )  # DA LINHA 243 À LINHA 244 ESTÁ SENDO CRIADO UM USUÁRIO 
        db.session.add(vagas) 
        db.session.commit()
        return gera_response(201, "vagas", vagas.to_json(), "Uma nova vaga adicionada com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "vagas", {}, "Erro ao cadastrar")


# ATUALIZANDO UMA VAGA 

@app.route("/vaga/<id>", methods=["PUT"])
def atualiza_vaga(id):
    vaga_objeto = vaga.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('cargo' in body):
            vaga_objeto.cargo = body['cargo']
        if('empresa' in body):
            vaga_objeto.empresa = body['empresa']
        if('local' in body):
            vaga_objeto.local = body['local']
        if('tipoVaga' in body):    
            vaga_objeto.tipoVaga = body['tipoVaga']

        db.session.add(vaga_objeto)
        db.session.commit()
        return gera_response(200, "vagas", vaga_objeto.to_json(), "Atualizado com sucesso!")
    except Exception as e:
        print(e)
    return gera_response(400, "experiencias", {}, "Erro ao atualizar")


# DELETANDO UMA VAGA

@app.route("/vaga/<id>", methods=["DELETE"])
def deleta_vaga(id):
    vaga_objeto = vaga.query.filter_by(id=id).first()

    try:
        db.session.delete(vaga_objeto)
        db.session.commit()
        return gera_response(200, "vagas", vaga_objeto.to_json(), "Vaga excluída com sucesso!")
    except Exception as e:
        print(e)
        return gera_response(400, "vagas", {}, "Erro ao excluir")



# INICIANDO A API DOS IMIGRANTES

class usuarioVaga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    vaga_id = db.Column(db.Integer, db.ForeignKey('vaga.id'))



    def to_json(self):
        return { "id":self.id, "usuario_id":self.usuario_id, "vaga_id":self.vaga_id }


# SELECIONANDO TODAS AS VAGAS CANDIDATAS PELO USUÁRIO

@app.route("/vagadeusuarios", methods=["GET"])
def seleciona_usuarioVagas():    
    usuarioVagas_objetos = usuarioVaga.query.all()
    usuarioVagas_json = [usuarioVaga.to_json() for usuarioVaga in usuarioVagas_objetos]
    print(usuarioVagas_json)

    return gera_response(200, "usuarioVagas", usuarioVagas_json, "ok")

# SELECIONANDO SOMENTE UMA VAGA CANDIDATA PELO USUÁRIO

@app.route("/vagadeusuario/<id>", methods=["GET"])
def seleciona_usuariovaga(id):
    vagas_objeto = usuarioVaga.query.filter_by(id=id).first()
    vagas_json = vagas_objeto.to_json()

    return gera_response(200, "vagas", vagas_json)

# CANDIDANTO A UMA NOVA VAGA

@app.route("/vagadeusuario", methods=["POST"])
def cria_vagausuario():
    body = request.get_json()

    try:
        vagausuarios = usuarioVaga(usuario_id=body["usuario_id"], vaga_id=body["vaga_id"])  
        db.session.add(vagausuarios) 
        db.session.commit()
        return gera_response(201, "vagausuarios", vagausuarios.to_json(), "Candidato com sucesso a uma nova vaga")
    except Exception as e:
        print(e)
        return gera_response(400, "vagausuarios", {}, "Erro ao cadastrar")



# ATUALIZANDO UMA CANDIDATURA 

@app.route("/vagadeusuario/<id>", methods=["PUT"])
def atualiza_vagausuario(id):
    vagausuario_objeto = usuarioVaga.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('usuario_id' in body):
            vagausuario_objeto.usuario_id = body['usuario_id']
        if('vaga_id' in body):
            vagausuario_objeto.vaga_id = body['vaga_id']
        
        db.session.add(vagausuario_objeto)
        db.session.commit()
        return gera_response(200, "vagausuarios", vagausuario_objeto.to_json(), "Atualizado com sucesso!")
    except Exception as e:
        print(e)
    return gera_response(400, "vagausuarios", {}, "Erro ao atualizar")


# DELETANDO UMA VAGA CANDIDATA

@app.route("/vagadeusuario/<id>", methods=["DELETE"])
def deleta_vagausuario(id):
    vagausuario_objeto = usuarioVaga.query.filter_by(id=id).first()

    try:
        db.session.delete(vagausuario_objeto)
        db.session.commit()
        return gera_response(200, "vagausuarios", vagausuario_objeto.to_json(), "Candidatura excluída com sucesso!")
    except Exception as e:
        print(e)
        return gera_response(400, "vagausuarios", {}, "Erro ao excluir")




def gera_response(status, nomeCoteudo, conteudo, mensagem=False):
    body = {}
    body [nomeCoteudo] = conteudo 

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

app.run()