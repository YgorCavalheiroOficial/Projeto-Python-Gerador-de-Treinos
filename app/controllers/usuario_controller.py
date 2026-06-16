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

    def listar_todos(self):
        return self.db.query(Usuario).all()

    def deletar(self, usuario_id):
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if usuario:
            self.db.delete(usuario)
            self.db.commit()