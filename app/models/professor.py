from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base  # Certifique-se de que sua classe Base está em base.py

class Professor(Base):
    __tablename__ = 'professores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)  

    # Relacionamento 1 para Muitos com Alunos (Usuario)
    alunos = relationship("Usuario", back_populates="professor", cascade="all, delete-orphan")