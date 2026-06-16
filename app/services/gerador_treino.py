from app.models.usuario import Usuario
from app.models.exercicio import Exercicio
from app.models.plano_treino import PlanoTreino, ItemTreino
from sqlalchemy.orm import Session

class GeradorTreinoService:
    @staticmethod
    def gerar_plano(db: Session, usuario: Usuario) -> PlanoTreino:
        """
        Algoritmo inteligente de prescrição (Além do CRUD).
        Avalia biotipo e objetivos para definir volume, repetições e descanso.
        """
        # 1. Define parâmetros de treino conforme o Biotipo
        biotipo = usuario.biotipo.upper()
        if "ECTOMORFO" in biotipo:
            series = 3
            repeticoes = 8
            descanso = 120  # Mais tempo de descanso para cargas maiores
            divisao = "ABC"
        elif "ENDOMORFO" in biotipo:
            series = 4
            repeticoes = 15
            descanso = 45   # Menos descanso para manter frequência cardíaca alta
            divisao = "ABCD"
        else:  # Mesomorfo
            series = 4
            repeticoes = 10
            descanso = 90
            divisao = "ABC"

        # 2. Instancia o Plano Base
        plano = PlanoTreino(usuario_id=usuario.id, divisao_treino=divisao)
        db.add(plano)
        db.flush()  # Gera ID temporário para o plano

        # 3. Busca exercícios cadastrados para popular o treino
        exercicios = db.query(Exercicio).all()
        
        # Se não houver exercícios cadastrados, cria alguns básicos para o MVP rodar limpo
        if not exercicios:
            basicos = [
                Exercicio(nome="Supino Reto", grupo_muscular="Peito", descricao="Barra livre"),
                Exercicio(nome="Puxada Frente", grupo_muscular="Costas", descricao="Na polia"),
                Exercicio(nome="Agachamento Livre", grupo_muscular="Pernas", descricao="Com barra"),
                Exercicio(nome="Desenvolvimento", grupo_muscular="Ombros", descricao="Com halteres")
            ]
            db.add_all(basicos)
            db.flush()
            exercicios = basicos

        # 4. Aloca os exercícios dentro do plano gerado
        for ex in exercicios:
            item = ItemTreino(
                plano_id=plano.id,
                exercicio_id=ex.id,
                series=series,
                repeticoes=repeticoes,
                descanso_segundos=descanso
            )
            db.add(item)
        
        db.commit()
        return plano