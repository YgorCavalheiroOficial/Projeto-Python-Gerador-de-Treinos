"""Controller responsável pela autenticação de professores no FitLogic."""

import hashlib
from app.config import SessionLocal
from app.models.professor import Professor
from app.models.session_manager import SessionManager

class AuthController:
    """Camada de controle responsável pelo fluxo de login do sistema.

    Faz a ponte entre a :class:`~app.views.login_view.LoginView` e a
    persistência de :class:`~app.models.professor.Professor`, validando
    credenciais e delegando o registro da sessão ao
    :class:`~app.models.session_manager.SessionManager`.
    """

    def __init__(self):
        """Inicializa o controller abrindo uma nova sessão de banco de dados."""
        self.db = SessionLocal()

    def _hash_senha(self, senha: str) -> str:
        """Gera o hash SHA-256 de uma senha em texto puro.

        Args:
            senha (str): Senha informada pelo usuário no formulário de login.

        Returns:
            str: Representação hexadecimal do hash SHA-256 da senha.
        """
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()

    def login(self, email, senha) -> bool:
        """Valida as credenciais informadas e autentica o professor.

        Calcula o hash da senha recebida e busca um professor cujo e-mail e
        senha (hash) correspondam exatamente ao informado. Em caso de
        sucesso, registra a sessão ativa via :class:`SessionManager`.

        Args:
            email (str): E-mail informado no formulário de login.
            senha (str): Senha em texto puro informada pelo usuário.

        Returns:
            bool: ``True`` se as credenciais forem válidas e o login for
                efetuado com sucesso, ``False`` caso contrário.
        """
        senha_crypto = self._hash_senha(senha)
        
        professor = self.db.query(Professor).filter_by(email=email, senha=senha_crypto).first()
        if professor:
            SessionManager.login(professor_id=professor.id, nome=professor.nome)
            return True
        return False