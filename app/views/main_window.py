import customtkinter as ctk
from app.views.usuario_view import UsuarioView
from app.views.exercicio_view import ExercicioView
from app.views.treino_view import TreinoView

class MainWindow(ctk.CTk):
    def __init__(self):
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
        # Sidebar Esquerda
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        lbl_logo = ctk.CTkLabel(self.sidebar, text="FitLogic v1.0", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_logo.pack(pady=30, padx=20)

        # Botões do Menu com consistência visual
        self.btn_usuarios = ctk.CTkButton(self.sidebar, text="Alunos (Ctrl+U)", anchor="w", height=40, command=lambda: self.exibir_aba("usuarios"))
        self.btn_usuarios.pack(fill="x", padx=15, pady=5)

        self.btn_exercicios = ctk.CTkButton(self.sidebar, text="Exercícios (Ctrl+E)", anchor="w", height=40, command=lambda: self.exibir_aba("exercicios"))
        self.btn_exercicios.pack(fill="x", padx=15, pady=5)

        self.btn_treinos = ctk.CTkButton(self.sidebar, text="Gerar Treinos (Ctrl+T)", anchor="w", height=40, command=lambda: self.exibir_aba("treinos"))
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
        """Alterna dinamicamente os frames na tela garantindo consistência estrutural."""
        for name, view in self.views.items():
            if name == nome_aba:
                view.pack(fill="both", expand=True)
                # Destaca botão ativo
                getattr(self, f"btn_{name}").configure(fg_color="#1976D2")
            else:
                view.pack_forget()
                getattr(self, f"btn_{name}").configure(fg_color=["#3B8ED0", "#1F538D"])

    def configurar_atalhos(self):
        """Mapeamento global de teclas de atalho exigido no projeto desktop."""
        self.bind("<Control-u>", lambda e: self.exibir_aba("usuarios"))
        self.bind("<Control-e>", lambda e: self.exibir_aba("exercicios"))
        self.bind("<Control-t>", lambda e: self.exibir_aba("treinos"))