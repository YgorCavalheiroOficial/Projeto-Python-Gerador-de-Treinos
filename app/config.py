"""Configuração de infraestrutura de persistência da aplicação FitLogic.

Este módulo concentra a configuração do SQLAlchemy (engine, fábrica de
sessões) e as rotinas de inicialização do banco de dados SQLite utilizado
pelo sistema, incluindo a criação das tabelas mapeadas pelo ORM e a
inserção de um registro de teste (seed) na primeira execução.
"""

import os
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.professor import Professor # Importa a model para verificar/criar o registro

DATABASE_URL = "sqlite:///fitlogic.db"
"""str: URL de conexão do banco de dados relacional SQLite utilizado pela aplicação."""

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
"""Engine do SQLAlchemy responsável pela comunicação de baixo nível com o banco SQLite."""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""sessionmaker: Fábrica de sessões ORM utilizada pelos controllers para acessar o banco."""

def popular_dados_teste():
    """Garante que exista pelo menos um professor cadastrado para testes.

    Verifica se a tabela de professores está vazia e, em caso positivo,
    insere um registro padrão (login: ``admin@fitlogic.com`` / senha:
    ``admin123``, armazenada com hash SHA-256) para permitir o primeiro
    acesso ao sistema sem necessidade de cadastro manual prévio.

    Side Effects:
        Realiza commit ou rollback na sessão do banco de dados e a fecha
        ao final da execução.
    """
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
    """Inicializa a estrutura do banco de dados relacional.

    Cria todas as tabelas mapeadas pelos modelos do SQLAlchemy (caso ainda
    não existam) e, em seguida, aciona a rotina de seed
    (:func:`popular_dados_teste`) para garantir que exista ao menos um
    professor cadastrado para fins de teste/demonstração.

    Raises:
        Exception: Qualquer erro de baixo nível do SQLAlchemy/SQLite é
            capturado e registrado via ``print``, não sendo repropagado.
    """
    try:
        # Garante a criação estrutural das tabelas mapeadas no ORM
        Base.metadata.create_all(bind=engine)
        print("Banco de dados inicializado com sucesso.")
        
        # Executa a semente de teste logo após certificar as tabelas
        popular_dados_teste()
        
    except Exception as e:
        print(f"Erro crítico ao inicializar o banco de dados: {e}")