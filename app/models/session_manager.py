"""Gerenciamento da sessão de autenticação em memória do FitLogic."""

class SessionManager:
    """Mantém em memória os dados do professor autenticado na sessão atual.

    Implementa um estado global simples (via atributos de classe) que
    substitui a necessidade de uma sessão de servidor, já que o FitLogic é
    uma aplicação desktop single-user por execução. É consultado pelos
    controllers para isolar os dados de cada professor/personal trainer
    (ex.: listar apenas os alunos do professor logado).

    Attributes:
        _usuario_logado (dict | None): Dicionário ``{"id": int, "nome": str}``
            do professor atualmente autenticado, ou ``None`` se não houver
            ninguém logado.
    """

    _usuario_logado = None

    @classmethod
    def login(cls, professor_id, nome):
        """Registra o professor autenticado na sessão atual.

        Args:
            professor_id (int): Identificador do professor autenticado.
            nome (str): Nome do professor, usado para exibição na interface.
        """
        cls._usuario_logado = {"id": professor_id, "nome": nome}

    @classmethod
    def logout(cls):
        """Encerra a sessão atual, removendo os dados do usuário logado."""
        cls._usuario_logado = None

    @classmethod
    def get_usuario_logado(cls):
        """Retorna os dados do professor autenticado na sessão atual.

        Returns:
            dict | None: Dicionário ``{"id": int, "nome": str}`` do
                professor logado, ou ``None`` caso nenhum login tenha sido
                realizado.
        """
        return cls._usuario_logado