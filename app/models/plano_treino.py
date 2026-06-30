"""Entidades de domínio PlanoTreino e ItemTreino.

Modelam a ficha de treino gerada pelo sistema para um usuário, com sua
divisão semanal (ex.: ABC, ABCD) e os exercícios prescritos em cada item,
incluindo o volume de séries/repetições e o tempo de descanso calculados
pelo algoritmo de :class:`app.services.gerador_treino.GeradorTreinoService`.
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import date

class PlanoTreino(Base):
    """Representa um plano (ficha) de treino gerado para um usuário.

    Um plano agrega vários :class:`ItemTreino`, cada um associando um
    exercício do catálogo aos parâmetros de séries, repetições e descanso
    definidos para aquele usuário.

    Attributes:
        id (int): Identificador único do plano (chave primária).
        usuario_id (int): Chave estrangeira para o usuário dono do plano.
        data_criacao (date): Data em que o plano foi gerado (padrão: hoje).
        divisao_treino (str): Divisão semanal do treino (ex.: "ABC", "ABCD").
        usuario (Usuario): Relacionamento com o usuário associado ao plano.
        itens (list[ItemTreino]): Itens (exercícios prescritos) que compõem
            o plano. Excluídos em cascata junto com o plano.
    """

    __tablename__ = "planos_treino"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    data_criacao = Column(Date, default=date.today)
    divisao_treino = Column(String(10), nullable=False)  # Ex: ABC, ABCD

    # Relacionamentos
    usuario = relationship("Usuario")
    itens = relationship("ItemTreino", back_populates="plano", cascade="all, delete-orphan")

class ItemTreino(Base):
    """Representa um exercício prescrito dentro de um plano de treino.

    Attributes:
        id (int): Identificador único do item (chave primária).
        plano_id (int): Chave estrangeira para o :class:`PlanoTreino` ao
            qual este item pertence.
        exercicio_id (int): Chave estrangeira para o :class:`~app.models.exercicio.Exercicio`
            prescrito.
        series (int): Número de séries calculado pelo algoritmo de geração.
        repeticoes (int): Número de repetições por série.
        descanso_segundos (int): Tempo de descanso recomendado entre séries,
            em segundos.
        plano (PlanoTreino): Relacionamento reverso com o plano de treino.
        exercicio (Exercicio): Relacionamento com o exercício prescrito.
    """

    __tablename__ = "itens_treino"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plano_id = Column(Integer, ForeignKey("planos_treino.id", ondelete="CASCADE"), nullable=False)
    exercicio_id = Column(Integer, ForeignKey("exercicios.id", ondelete="CASCADE"), nullable=False)
    series = Column(Integer, nullable=False)
    repeticoes = Column(Integer, nullable=False)
    descanso_segundos = Column(Integer, nullable=False)

    # Relacionamentos
    plano = relationship("PlanoTreino", back_populates="itens")
    exercicio = relationship("Exercicio")