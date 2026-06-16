from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import date

class PlanoTreino(Base):
    __tablename__ = "planos_treino"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    data_criacao = Column(Date, default=date.today)
    divisao_treino = Column(String(10), nullable=False)  # Ex: ABC, ABCD

    # Relacionamentos
    usuario = relationship("Usuario")
    itens = relationship("ItemTreino", back_populates="plano", cascade="all, delete-orphan")

class ItemTreino(Base):
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