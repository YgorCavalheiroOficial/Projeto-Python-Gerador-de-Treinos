"""Controller responsável pela geração e exportação de planos de treino."""

from app.config import SessionLocal
from app.models.plano_treino import PlanoTreino
from app.models.usuario import Usuario
from app.services.gerador_treino import GeradorTreinoService
from app.services.gerador_pdf import GeradorPDFService

class TreinoController:
    """Camada de controle para a geração inteligente de treinos.

    Coordena o :class:`~app.services.gerador_treino.GeradorTreinoService`
    (regras de negócio de prescrição de treino) e o
    :class:`~app.services.gerador_pdf.GeradorPDFService` (exportação em
    PDF), expondo as operações utilizadas pela
    :class:`~app.views.treino_view.TreinoView`.
    """

    def __init__(self):
        """Inicializa o controller abrindo uma nova sessão de banco de dados."""
        self.db = SessionLocal()

    def gerar_novo_treino(self, usuario_id):
        """Gera um novo plano de treino personalizado para um usuário.

        Args:
            usuario_id (int): Identificador do usuário (aluno) para o qual
                o treino será gerado.

        Returns:
            PlanoTreino | None: O plano de treino recém-gerado, ou ``None``
                se o usuário informado não existir.
        """
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            return None
        return GeradorTreinoService.gerar_plano(self.db, usuario)

    def listar_planos_usuario(self, usuario_id):
        """Lista todos os planos de treino já gerados para um usuário.

        Args:
            usuario_id (int): Identificador do usuário (aluno).

        Returns:
            list[PlanoTreino]: Lista de planos de treino do usuário,
                ordenados conforme retornados pela consulta ao banco.
        """
        return self.db.query(PlanoTreino).filter(PlanoTreino.usuario_id == usuario_id).all()

    def baixar_pdf(self, plano_id, caminho_salvar):
        """Exporta um plano de treino para um arquivo PDF.

        Args:
            plano_id (int): Identificador do plano de treino a ser exportado.
            caminho_salvar (str): Caminho completo (incluindo nome do
                arquivo) onde o PDF será salvo em disco.

        Returns:
            bool: ``True`` se o plano foi encontrado e o PDF gerado com
                sucesso, ``False`` se o plano informado não existir.
        """
        plano = self.db.query(PlanoTreino).filter(PlanoTreino.id == plano_id).first()
        if plano:
            GeradorPDFService.exportar_treino(plano, caminho_salvar)
            return True
        return False