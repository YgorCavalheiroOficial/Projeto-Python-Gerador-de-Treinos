"""Ponto de entrada da aplicação FitLogic.

Orquestra a inicialização da infraestrutura (idioma e banco de dados) e o
fluxo de telas, abrindo primeiro a tela de login e, após autenticação
bem-sucedida, a janela principal do sistema.
"""

import logging
from tkinter import messagebox
from app.config import inicializar_banco
from app.services.locale_manager import LocaleManager
from app.views.main_window import MainWindow
from app.views.login_view import LoginView 
from app.config import inicializar_banco, popular_dados_teste

# Configuração do sistema de logs para monitorizar o fluxo da aplicação
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def abrir_sistema_principal():
    """
    Função de callback que será disparada pela LoginView 
    apenas quando o login for validado com sucesso.
    """
    logging.info("Autenticação bem-sucedida! Renderizando a interface principal...")
    try:
        app = MainWindow()
        app.mainloop()
        logging.info("Aplicação encerrada normalmente pelo usuário.")
    except Exception as erro_interface:
        logging.error(f"Erro inesperado na interface principal: {erro_interface}", exc_info=True)

def preparar_ambiente() -> bool:
    """Executa as rotinas de infraestrutura (Locale e Banco de Dados)."""
    try:
        # 1. Detecta e inicializa o idioma do sistema
        LocaleManager.inicializar()
        
        # 2. Inicializa as tabelas do banco de dados (SQLite + SQLAlchemy)
        logging.info("Inicializando persistência relacional (SQLite + SQLAlchemy)...")
        inicializar_banco()

        # 3. Injeta o usuário de testes caso o banco esteja zerado
        popular_dados_teste()
        
        return True
    except Exception as erro:
        logging.critical(f"Falha fatal ao preparar o ambiente: {erro}", exc_info=True)
        messagebox.showerror(
            "Erro de Inicialização",
            f"Não foi possível iniciar o sistema FitLogic.\n\nDetalhe técnico: {erro}"
        )
        return False

def main():
    """Função principal: prepara o ambiente e inicia o fluxo de telas.

    Executa a validação/inicialização da infraestrutura
    (:func:`preparar_ambiente`) e, em caso de sucesso, abre a
    :class:`~app.views.login_view.LoginView`, que por sua vez aciona
    :func:`abrir_sistema_principal` após uma autenticação bem-sucedida.
    """
    # Executa a validação de infraestrutura
    if not preparar_ambiente():
        return

    logging.info("Iniciando a tela de autenticação do FitLogic...")
    try:
        # Instancia a LoginView passando a função 'abrir_sistema_principal' como callback de sucesso
        tela_login = LoginView(on_login_success=abrir_sistema_principal)
        tela_login.mainloop()
    except Exception as erro_login:
        logging.error(f"Erro crítico na execução da tela de login: {erro_login}", exc_info=True)

if __name__ == "__main__":
    main()