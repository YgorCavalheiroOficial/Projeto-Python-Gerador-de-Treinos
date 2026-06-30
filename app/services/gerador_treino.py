"""Serviço com o algoritmo de geração inteligente de planos de treino."""

from app.models.usuario import Usuario
from app.models.exercicio import Exercicio
from app.models.plano_treino import PlanoTreino, ItemTreino
from sqlalchemy.orm import Session

class GeradorTreinoService:
    """Concentra a regra de negócio de prescrição automática de treinos.

    Esta é a principal funcionalidade do sistema que vai além do CRUD
    básico: a partir do biotipo e do objetivo do usuário, o serviço decide
    a divisão semanal (ABC/ABCD), o volume de séries/repetições e o tempo
    de descanso ideal, então persiste um :class:`~app.models.plano_treino.PlanoTreino`
    completo, populado com os exercícios disponíveis no catálogo.
    """

    @staticmethod
    def gerar_plano(db: Session, usuario: Usuario) -> PlanoTreino:
        """Gera e persiste um novo plano de treino personalizado.

        Algoritmo inteligente de prescrição (além do CRUD): avalia o
        biotipo do usuário para decidir séries, repetições, descanso e a
        divisão de treino, popula o catálogo com exercícios básicos caso
        ele esteja vazio, e distribui os exercícios disponíveis dentro do
        plano gerado.

        Regras de negócio aplicadas por biotipo:
            * Ectomorfo: 3 séries x 8 repetições, 120s de descanso, divisão ABC.
            * Endomorfo: 4 séries x 15 repetições, 45s de descanso, divisão ABCD.
            * Mesomorfo (padrão): 4 séries x 10 repetições, 90s de descanso, divisão ABC.

        Args:
            db (Session): Sessão ativa do SQLAlchemy utilizada para
                consultar exercícios e persistir o plano gerado.
            usuario (Usuario): Usuário (aluno) para o qual o treino será
                gerado; seu atributo ``biotipo`` define os parâmetros do
                algoritmo.

        Returns:
            PlanoTreino: O plano de treino recém-criado e já persistido no
                banco, com todos os seus itens (:class:`~app.models.plano_treino.ItemTreino`)
                associados.
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