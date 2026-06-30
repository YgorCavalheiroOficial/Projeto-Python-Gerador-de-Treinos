"""Entidade de domínio Professor (personal trainer/professor responsável)."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base  # Certifique-se de que sua classe Base está em base.py

class Professor(Base):
    """Representa um professor/personal trainer autenticado no sistema.

    Cada professor possui um conjunto isolado de alunos (:class:`~app.models.usuario.Usuario`)
    e é o usuário que efetivamente realiza login no FitLogic
    (ver :class:`app.controllers.auth_controller.AuthController`).

    Attributes:
        id (int): Identificador único do professor (chave primária).
        nome (str): Nome completo do professor.
        email (str): E-mail utilizado como login, único no sistema.
        senha (str): Hash SHA-256 da senha de acesso (nunca armazenada em
            texto puro).
        alunos (list[Usuario]): Lista de alunos vinculados a este professor.
            Excluídos em cascata caso o professor seja removido.
    """

    __tablename__ = 'professores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)  

    # Relacionamento 1 para Muitos com Alunos (Usuario)
    alunos = relationship("Usuario", back_populates="professor", cascade="all, delete-orphan")