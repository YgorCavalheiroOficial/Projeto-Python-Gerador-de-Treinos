from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Exercicio(Base):
    __tablename__ = "exercicios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    grupo_muscular = Column(String(50), nullable=False)  # Peito, Costas, Pernas, etc.
    descricao = Column(String(255), nullable=True)