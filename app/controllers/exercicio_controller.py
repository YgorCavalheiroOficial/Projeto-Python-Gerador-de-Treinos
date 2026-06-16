from app.config import get_db
from app.models.exercicio import Exercicio

class ExercicioController:
    def __init__(self):
        self.db = get_db()

    def cadastrar(self, nome, grupo_muscular, descricao):
        exercicio = Exercicio(nome=nome, grupo_muscular=grupo_muscular, descricao=descricao)
        self.db.add(exercicio)
        self.db.commit()
        return exercicio

    def listar_todos(self):
        return self.db.query(Exercicio).all()

    def deletar(self, exercicio_id):
        ex = self.db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
        if ex:
            self.db.delete(ex)
            self.db.commit()