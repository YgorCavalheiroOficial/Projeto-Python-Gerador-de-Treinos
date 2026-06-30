"""Janela principal do FitLogic, exibida após autenticação bem-sucedida."""

import customtkinter as ctk
from app.views.usuario_view import UsuarioView
from app.views.exercicio_view import ExercicioView
from app.services.locale_manager import LocaleManager
from app.views.treino_view import TreinoView

class MainWindow(ctk.CTk):
    """Janela principal com navegação lateral entre as abas do sistema.

    Organiza a interface em uma barra lateral (sidebar) de navegação e um
    container central onde as views de Usuários, Exercícios e Treinos são
    alternadas dinamicamente, mantendo o padrão visual consistente exigido
    entre todas as telas e oferecendo atalhos de teclado para navegação.

    Attributes:
        sidebar (ctk.CTkFrame): Painel lateral com os botões de navegação.
        container (ctk.CTkFrame): Painel central onde as views são exibidas.
        views (dict[str, ctk.CTkFrame]): Mapa ``{nome_aba: instância da view}``
            com as três telas principais, mantidas em cache (instanciadas
            uma única vez).
    """

    def __init__(self):
        """Inicializa a janela principal, monta o layout e abre a aba inicial."""
        super().__init__()

        self.title("FitLogic - Sistema Integrado de Prescrição")
        self.geometry("1100x650")
        
        # Tema padrão escuro/azul consistente
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.setup_layout()
        self.configurar_atalhos()
        self.exibir_aba("usuarios")

    def setup_layout(self):
        """Monta a barra lateral de navegação e instancia as views principais."""
        # Sidebar Esquerda
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        lbl_logo = ctk.CTkLabel(self.sidebar, text="FitLogic v1.0", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_logo.pack(pady=30, padx=20)

        # Botões do Menu ancorados corretamente na self.sidebar
        # CORREÇÃO: Alterado de py=5 para pady=5
        self.btn_alunos = ctk.CTkButton(self.sidebar, text=LocaleManager.t("btn_nav_alunos"), anchor="w", height=40, command=lambda: self.exibir_aba("usuarios"))
        self.btn_alunos.pack(fill="x", padx=15, pady=5)

        self.btn_exercicios = ctk.CTkButton(self.sidebar, text=LocaleManager.t("btn_nav_exercicios"), anchor="w", height=40, command=lambda: self.exibir_aba("exercicios"))
        self.btn_exercicios.pack(fill="x", padx=15, pady=5)

        self.btn_treinos = ctk.CTkButton(self.sidebar, text=LocaleManager.t("btn_nav_treinos"), anchor="w", height=40, command=lambda: self.exibir_aba("treinos"))
        self.btn_treinos.pack(fill="x", padx=15, pady=5)

        # Container Principal Direito
        self.container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container.pack(side="right", fill="both", expand=True)

        # Inicialização das views em cache
        self.views = {
            "usuarios": UsuarioView(self.container),
            "exercicios": ExercicioView(self.container),
            "treinos": TreinoView(self.container)
        }

    def exibir_aba(self, nome_aba):
        """Alterna dinamicamente os frames na tela garantindo consistência estrutural.

        Exibe a view correspondente a ``nome_aba`` e oculta as demais,
        além de destacar visualmente o botão da aba ativa na sidebar.

        Args:
            nome_aba (str): Identificador da aba a ser exibida (``"usuarios"``,
                ``"exercicios"`` ou ``"treinos"``).
        """
        botoes_menu = {
            "usuarios": self.btn_alunos,
            "exercicios": self.btn_exercicios,
            "treinos": self.btn_treinos
        }

        for name, view in self.views.items():
            botao = botoes_menu.get(name)
            if name == nome_aba:
                view.pack(fill="both", expand=True)
                if botao:
                    botao.configure(fg_color="#1976D2")  # Cor de destaque do botão ativo
            else:
                view.pack_forget()
                if botao:
                    # CORREÇÃO: Uso de tupla ( ) no lugar de lista [ ] para não dar erro de Tcl
                    botao.configure(fg_color=("#3B8ED0", "#1F538D"))

    def configurar_atalhos(self):
        """Mapeamento global de teclas de atalho exigido no projeto desktop.

        Vincula ``Ctrl+U``, ``Ctrl+E`` e ``Ctrl+T`` à navegação direta para
        as abas de Usuários, Exercícios e Treinos, respectivamente,
        garantindo acessibilidade via teclado em toda a aplicação.
        """
        self.bind("<Control-u>", lambda e: self.exibir_aba("usuarios"))
        self.bind("<Control-e>", lambda e: self.exibir_aba("exercicios"))
        self.bind("<Control-t>", lambda e: self.exibir_aba("treinos"))