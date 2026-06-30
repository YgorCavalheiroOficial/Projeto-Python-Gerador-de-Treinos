from app.config import SessionLocal
from app.models.exercicio import Exercicio

class ExercicioController:
    def __init__(self):
        self.db = SessionLocal()

    def cadastrar(self, nome, grupo_muscular, descricao):
        exercicio = Exercicio(nome=nome, grupo_muscular=grupo_muscular, descricao=descricao)
        self.db.add(exercicio)
        self.db.commit()
        return exercicio

    def buscar_por_id(self, exercicio_id):
        return self.db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()

    def atualizar(self, exercicio_id, nome, grupo_muscular, descricao):
        ex = self.buscar_por_id(exercicio_id)
        if ex:
            ex.nome = nome
            ex.grupo_muscular = grupo_muscular
            ex.descricao = descricao
            self.db.commit()
            return ex
        return None

    def listar_todos(self):
        return self.db.query(Exercicio).all()

    def deletar(self, exercicio_id):
        ex = self.buscar_por_id(exercicio_id)
        if ex:
            self.db.delete(ex)
            self.db.commit()
            return True
        return False