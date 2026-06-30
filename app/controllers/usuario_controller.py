from app.config import SessionLocal
from app.models.usuario import Usuario
from app.models.session_manager import SessionManager

class UsuarioController:
    def __init__(self):
        self.db = SessionLocal()

    def cadastrar(self, nome, peso, altura, sexo, biotipo, objetivo, descricao):
        prof = SessionManager.get_usuario_logado()
        if not prof: return False
        
        try:
            novo_aluno = Usuario(
                nome=nome, peso=peso, altura=altura, sexo=sexo,
                biotipo=biotipo, objetivo=objetivo, descricao=descricao,
                professor_id=prof["id"] # Vincula ao logado
            )
            self.db.add(novo_aluno)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def buscar_por_id(self, usuario_id):
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def atualizar(self, usuario_id, nome, peso, altura, biotipo, objetivo, descricao):
        usuario = self.buscar_por_id(usuario_id)
        if usuario:
            usuario.nome = nome
            usuario.peso = float(peso)
            usuario.altura = float(altura)
            usuario.biotipo = biotipo
            usuario.objetivo = objetivo
            usuario.descricao = descricao
            self.db.commit()
            return usuario
        return None

    def listar_todos(self):
        prof = SessionManager.get_usuario_logado()
        if not prof: return []
        
        return self.db.query(Usuario).filter_by(professor_id=prof["id"]).all()

    def deletar(self, usuario_id):
        usuario = self.buscar_por_id(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False