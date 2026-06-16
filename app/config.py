import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base

# Define o caminho do banco de dados na raiz do projeto
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "fitlogic.db"))
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Inicialização do Engine do SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def inicializar_banco():
    """Importa todas as entidades e cria as tabelas se não existirem."""
    from app.models.usuario import Usuario
    from app.models.exercicio import Exercicio
    from app.models.plano_treino import PlanoTreino, ItemTreino
    Base.metadata.create_all(bind=engine)

def get_db():
    """Retorna uma nova sessão isolada com o banco de dados."""
    return SessionLocal()