import os
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.professor import Professor # Importa a model para verificar/criar o registro

DATABASE_URL = "sqlite:///fitlogic.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def popular_dados_teste():
    """Garante que exista pelo menos um professor cadastrado para testes."""
    db = SessionLocal()
    try:
        if db.query(Professor).count() == 0:
            senha_admin = hashlib.sha256("admin123".encode('utf-8')).hexdigest()
            
            professor_teste = Professor(
                nome="Treinador Admin",
                email="admin@fitlogic.com",
                senha=senha_admin
            )
            db.add(professor_teste)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"[SEED] Erro ao popular banco: {e}")
    finally:
        db.close()

def inicializar_banco():
    try:
        # Garante a criação estrutural das tabelas mapeadas no ORM
        Base.metadata.create_all(bind=engine)
        print("Banco de dados inicializado com sucesso.")
        
        # Executa a semente de teste logo após certificar as tabelas
        popular_dados_teste()
        
    except Exception as e:
        print(f"Erro crítico ao inicializar o banco de dados: {e}")