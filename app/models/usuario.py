"""Entidade de domínio Usuario (aluno/cliente do personal trainer)."""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Usuario(Base):
    """Representa um aluno cadastrado por um professor/personal trainer.

    Armazena o perfil antropométrico e os objetivos do aluno, utilizados
    pelo :class:`app.services.gerador_treino.GeradorTreinoService` para
    calcular automaticamente a divisão de treino, o volume de séries e o
    tempo de descanso mais adequados ao seu biotipo.

    Attributes:
        id (int): Identificador único do usuário (chave primária).
        nome (str): Nome completo do aluno.
        peso (float): Peso corporal em quilogramas.
        altura (float): Altura em metros.
        sexo (str): Sexo biológico informado pelo aluno.
        biotipo (str): Biotipo fisionômico (Ectomorfo, Mesomorfo ou
            Endomorfo), usado como principal critério do algoritmo de
            geração de treinos.
        objetivo (str): Objetivo principal do aluno (ex.: hipertrofia,
            emagrecimento, condicionamento).
        descricao (str): Observações adicionais, incluindo dores ou
            limitações físicas relatadas pelo aluno.
        professor_id (int): Chave estrangeira para o professor responsável.
        professor (Professor): Relacionamento com o professor que cadastrou
            este aluno.
    """

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
        """Calcula o Índice de Massa Corporal (IMC) do usuário.

        Aplica a fórmula padrão ``peso / altura²`` para estimar o IMC com
        base nos dados antropométricos cadastrados.

        Returns:
            float: O IMC calculado e arredondado para 2 casas decimais, ou
                ``0.0`` caso a altura cadastrada seja inválida (<= 0), para
                evitar uma divisão por zero.
        """
        if self.altura > 0:
            return round(self.peso / (self.altura ** 2), 2)
        return 0.0