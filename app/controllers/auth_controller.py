import hashlib
from app.config import SessionLocal
from app.models.professor import Professor
from app.models.session_manager import SessionManager

class AuthController:
    def __init__(self):
        self.db = SessionLocal()

    def _hash_senha(self, senha: str) -> str:
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()

    def login(self, email, senha) -> bool:
        senha_crypto = self._hash_senha(senha)
        
        professor = self.db.query(Professor).filter_by(email=email, senha=senha_crypto).first()
        if professor:
            SessionManager.login(professor_id=professor.id, nome=professor.nome)
            return True
        return False