from app.config import get_db
from app.models.usuario import Usuario

class UsuarioController:
    def __init__(self):
        self.db = get_db()

    def cadastrar(self, nome, peso, altura, sexo, biotipo, objetivo):
        usuario = Usuario(nome=nome, peso=float(peso), altura=float(altura), sexo=sexo, biotipo=biotipo, objetivo=objetivo)
        self.db.add(usuario)
        self.db.commit()
        return usuario

    def buscar_por_id(self, usuario_id):
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def atualizar(self, usuario_id, nome, peso, altura, biotipo, objetivo):
        usuario = self.buscar_por_id(usuario_id)
        if usuario:
            usuario.nome = nome
            usuario.peso = float(peso)
            usuario.altura = float(altura)
            usuario.biotipo = biotipo
            usuario.objetivo = objetivo
            self.db.commit()
            return usuario
        return None

    def listar_todos(self):
        return self.db.query(Usuario).all()

    def deletar(self, usuario_id):
        usuario = self.buscar_por_id(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False