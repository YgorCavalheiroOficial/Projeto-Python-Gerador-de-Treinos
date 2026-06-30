"""Controller de CRUD da entidade Exercicio (catálogo de exercícios)."""

from app.config import SessionLocal
from app.models.exercicio import Exercicio

class ExercicioController:
    """Camada de controle para o gerenciamento do catálogo de exercícios.

    Concentra as operações de criação, leitura, atualização e remoção
    (CRUD) da entidade :class:`~app.models.exercicio.Exercicio`, servindo
    de intermediário entre a :class:`~app.views.exercicio_view.ExercicioView`
    e a camada de persistência (SQLAlchemy).
    """

    def __init__(self):
        """Inicializa o controller abrindo uma nova sessão de banco de dados."""
        self.db = SessionLocal()

    def cadastrar(self, nome, grupo_muscular, descricao):
        """Cadastra um novo exercício no catálogo.

        Args:
            nome (str): Nome do exercício (deve ser único no catálogo).
            grupo_muscular (str): Grupo muscular principal trabalhado.
            descricao (str): Descrição opcional sobre a execução.

        Returns:
            Exercicio: A instância do exercício recém-criado e persistido.
        """
        exercicio = Exercicio(nome=nome, grupo_muscular=grupo_muscular, descricao=descricao)
        self.db.add(exercicio)
        self.db.commit()
        return exercicio

    def buscar_por_id(self, exercicio_id):
        """Busca um exercício pelo seu identificador.

        Args:
            exercicio_id (int): Identificador único do exercício.

        Returns:
            Exercicio | None: O exercício encontrado, ou ``None`` se não
                existir nenhum registro com o ID informado.
        """
        return self.db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()

    def atualizar(self, exercicio_id, nome, grupo_muscular, descricao):
        """Atualiza os dados de um exercício existente.

        Args:
            exercicio_id (int): Identificador do exercício a ser atualizado.
            nome (str): Novo nome do exercício.
            grupo_muscular (str): Novo grupo muscular.
            descricao (str): Nova descrição.

        Returns:
            Exercicio | None: O exercício atualizado, ou ``None`` caso o
                identificador informado não corresponda a nenhum registro.
        """
        ex = self.buscar_por_id(exercicio_id)
        if ex:
            ex.nome = nome
            ex.grupo_muscular = grupo_muscular
            ex.descricao = descricao
            self.db.commit()
            return ex
        return None

    def listar_todos(self):
        """Lista todos os exercícios cadastrados no catálogo.

        Returns:
            list[Exercicio]: Lista com todos os exercícios persistidos.
        """
        return self.db.query(Exercicio).all()

    def deletar(self, exercicio_id):
        """Remove um exercício do catálogo.

        Args:
            exercicio_id (int): Identificador do exercício a ser removido.

        Returns:
            bool: ``True`` se o exercício foi encontrado e removido,
                ``False`` caso não exista um registro com o ID informado.
        """
        ex = self.buscar_por_id(exercicio_id)
        if ex:
            self.db.delete(ex)
            self.db.commit()
            return True
        return False