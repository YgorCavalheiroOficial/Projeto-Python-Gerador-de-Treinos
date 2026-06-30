"""Entidade de domínio Exercicio (catálogo de exercícios de musculação)."""

from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Exercicio(Base):
    """Representa um exercício físico cadastrado no catálogo do sistema.

    Cada exercício pertence a um grupo muscular e é utilizado pelo motor
    de geração de treinos (:class:`app.services.gerador_treino.GeradorTreinoService`)
    para compor automaticamente os planos de treino dos usuários.

    Attributes:
        id (int): Identificador único do exercício (chave primária).
        nome (str): Nome do exercício (ex.: "Supino Reto"), único no catálogo.
        grupo_muscular (str): Grupo muscular trabalhado (ex.: Peito, Costas,
            Pernas, Bíceps, Tríceps, Ombros, Cárdio).
        descricao (str | None): Breve descrição opcional sobre a execução
            correta do exercício.
    """

    __tablename__ = "exercicios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    grupo_muscular = Column(String(50), nullable=False)  # Peito, Costas, Pernas, etc.
    descricao = Column(String(255), nullable=True)