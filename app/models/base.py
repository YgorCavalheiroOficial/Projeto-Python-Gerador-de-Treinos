"""Base declarativa do ORM utilizada por todas as entidades do FitLogic."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
"""sqlalchemy.orm.DeclarativeMeta: Classe base declarativa compartilhada por
todos os modelos (entidades) do sistema (Usuario, Exercicio, PlanoTreino,
Professor, etc.), permitindo que o SQLAlchemy mapeie cada subclasse para
uma tabela do banco de dados relacional.
"""