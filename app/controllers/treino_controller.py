from app.config import get_db
from app.models.plano_treino import PlanoTreino
from app.models.usuario import Usuario
from app.services.gerador_treino import GeradorTreinoService
from app.services.gerador_pdf import GeradorPDFService

class TreinoController:
    def __init__(self):
        self.db = get_db()

    def gerar_novo_treino(self, usuario_id):
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            return None
        return GeradorTreinoService.gerar_plano(self.db, usuario)

    def listar_planos_usuario(self, usuario_id):
        return self.db.query(PlanoTreino).filter(PlanoTreino.usuario_id == usuario_id).all()

    def baixar_pdf(self, plano_id, caminho_salvar):
        plano = self.db.query(PlanoTreino).filter(PlanoTreino.id == plano_id).first()
        if plano:
            GeradorPDFService.exportar_treino(plano, caminho_salvar)
            return True
        return False