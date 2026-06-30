"""Controller de CRUD da entidade Usuario (alunos do professor logado)."""

from app.config import SessionLocal
from app.models.usuario import Usuario
from app.models.session_manager import SessionManager

class UsuarioController:
    """Camada de controle para o gerenciamento de alunos (Usuario).

    Todas as operações são automaticamente filtradas/vinculadas ao
    professor autenticado na sessão atual (via
    :class:`~app.models.session_manager.SessionManager`), garantindo que
    cada professor só visualize e manipule seus próprios alunos.
    """

    def __init__(self):
        """Inicializa o controller abrindo uma nova sessão de banco de dados."""
        self.db = SessionLocal()

    def cadastrar(self, nome, peso, altura, sexo, biotipo, objetivo, descricao):
        """Cadastra um novo aluno vinculado ao professor logado.

        Args:
            nome (str): Nome completo do aluno.
            peso (float): Peso corporal em quilogramas.
            altura (float): Altura em metros.
            sexo (str): Sexo biológico do aluno.
            biotipo (str): Biotipo fisionômico (Ectomorfo, Mesomorfo ou
                Endomorfo).
            objetivo (str): Objetivo principal do treino.
            descricao (str): Observações adicionais, dores ou limitações.

        Returns:
            bool: ``True`` se o cadastro foi realizado com sucesso,
                ``False`` se não houver professor autenticado na sessão ou
                se ocorrer algum erro de persistência.
        """
        prof = SessionManager.get_usuario_logado()
        if not prof: return False
        
        try:
            novo_aluno = Usuario(
                nome=nome, peso=peso, altura=altura, sexo=sexo,
                biotipo=biotipo, objetivo=objetivo, descricao=descricao,
                professor_id=prof["id"] # Vincula ao logado
            )
            self.db.add(novo_aluno)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def buscar_por_id(self, usuario_id):
        """Busca um aluno pelo seu identificador.

        Args:
            usuario_id (int): Identificador único do aluno.

        Returns:
            Usuario | None: O aluno encontrado, ou ``None`` se não existir
                nenhum registro com o ID informado.
        """
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def atualizar(self, usuario_id, nome, peso, altura, biotipo, objetivo, descricao):
        """Atualiza os dados cadastrais de um aluno existente.

        Args:
            usuario_id (int): Identificador do aluno a ser atualizado.
            nome (str): Novo nome completo.
            peso (float | str): Novo peso corporal em quilogramas.
            altura (float | str): Nova altura em metros.
            biotipo (str): Novo biotipo fisionômico.
            objetivo (str): Novo objetivo principal.
            descricao (str): Novas observações/limitações.

        Returns:
            Usuario | None: O aluno atualizado, ou ``None`` caso o
                identificador informado não corresponda a nenhum registro.
        """
        usuario = self.buscar_por_id(usuario_id)
        if usuario:
            usuario.nome = nome
            usuario.peso = float(peso)
            usuario.altura = float(altura)
            usuario.biotipo = biotipo
            usuario.objetivo = objetivo
            usuario.descricao = descricao
            self.db.commit()
            return usuario
        return None

    def listar_todos(self):
        """Lista todos os alunos vinculados ao professor logado.

        Returns:
            list[Usuario]: Lista de alunos do professor autenticado, ou
                lista vazia caso não haja nenhum professor logado na sessão.
        """
        prof = SessionManager.get_usuario_logado()
        if not prof: return []
        
        return self.db.query(Usuario).filter_by(professor_id=prof["id"]).all()

    def deletar(self, usuario_id):
        """Remove um aluno do sistema.

        Args:
            usuario_id (int): Identificador do aluno a ser removido.

        Returns:
            bool: ``True`` se o aluno foi encontrado e removido, ``False``
                caso não exista um registro com o ID informado.
        """
        usuario = self.buscar_por_id(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False