class SessionManager:
    _usuario_logado = None

    @classmethod
    def login(cls, professor_id, nome):
        cls._usuario_logado = {"id": professor_id, "nome": nome}

    @classmethod
    def logout(cls):
        cls._usuario_logado = None

    @classmethod
    def get_usuario_logado(cls):
        return cls._usuario_logado