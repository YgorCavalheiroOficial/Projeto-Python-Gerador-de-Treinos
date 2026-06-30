from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    sexo = Column(String(20), nullable=False)
    biotipo = Column(String(20), nullable=False) 
    objetivo = Column(String(50), nullable=False) 
    descricao = Column(String(500), nullable=False)

    # Relacionamento: Vincula o Aluno ao Professor
    professor_id = Column(Integer, ForeignKey('professores.id'), nullable=False)
    professor = relationship("Professor", back_populates="alunos")

    def calcular_imc(self) -> float:
        """Calcula o Índice de Massa Corporal do usuário."""
        if self.altura > 0:
            return round(self.peso / (self.altura ** 2), 2)
        return 0.0