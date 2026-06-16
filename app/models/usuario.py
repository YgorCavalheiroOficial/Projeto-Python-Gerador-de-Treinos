from sqlalchemy import Column, Integer, String, Float
from app.models.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    sexo = Column(String(20), nullable=False)
    biotipo = Column(String(20), nullable=False)  # Ectomorfo, Mesomorfo, Endomorfo
    objetivo = Column(String(50), nullable=False)  # Hipertrofia, Emagrecimento, Resistência

    def calcular_imc(self) -> float:
        """Calcula o Índice de Massa Corporal do usuário."""
        if self.altura > 0:
            return round(self.peso / (self.altura ** 2), 2)
        return 0.0