"""Tela de autenticação (login) do FitLogic."""

import customtkinter as ctk
from tkinter import messagebox
from app.controllers.auth_controller import AuthController
from app.models.session_manager import SessionManager
from app.services.locale_manager import LocaleManager

class LoginView(ctk.CTk):
    """Janela inicial de login, exibida antes de qualquer outra tela.

    Coleta e-mail/senha do professor, delega a validação ao
    :class:`~app.controllers.auth_controller.AuthController` e, em caso de
    sucesso, fecha-se e aciona o callback ``on_login_success`` (responsável
    por abrir a :class:`~app.views.main_window.MainWindow`).

    Attributes:
        on_login_success (Callable): Função de callback chamada após um
            login bem-sucedido.
        controller (AuthController): Controller responsável por validar as
            credenciais informadas.
    """

    def __init__(self, on_login_success, **kwargs):
        """Inicializa a janela de login.

        Args:
            on_login_success (Callable): Função sem argumentos a ser
                chamada quando o login for validado com sucesso.
            **kwargs: Argumentos adicionais repassados ao construtor de
                ``ctk.CTk``.
        """
        super().__init__(**kwargs)
        
        # Garante a inicialização do idioma correspondente ao sistema operacional
        LocaleManager.inicializar()
        
        self.on_login_success = on_login_success
        self.controller = AuthController()
        
        self.title(LocaleManager.t("login_janela"))
        self.geometry("400x480")
        self.resizable(False, False)
        
        self.setup_ui()

    def setup_ui(self):
        """Monta os widgets da tela de login (campos de e-mail, senha e botão)."""
        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(pady=30, padx=30, fill="both", expand=True)

        ctk.CTkLabel(frame, text="FitLogic v1.0", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(30, 5))
        ctk.CTkLabel(frame, text=LocaleManager.t("login_subtitulo"), font=ctk.CTkFont(size=13)).pack(pady=(0, 25))

        self.txt_email = ctk.CTkEntry(frame, placeholder_text=LocaleManager.t("login_email"), width=260, height=40)
        self.txt_email.pack(pady=10)

        self.txt_senha = ctk.CTkEntry(frame, placeholder_text=LocaleManager.t("login_senha"), show="*", width=260, height=40)
        self.txt_senha.pack(pady=10)

        btn_entrar = ctk.CTkButton(frame, text=LocaleManager.t("btn_entrar"), width=260, height=42, fg_color="#1F538D", command=self.fazer_login)
        btn_entrar.pack(pady=(25, 10))

    def fazer_login(self):
        """Valida os campos preenchidos e tenta autenticar o professor.

        Exibe um aviso caso e-mail ou senha estejam vazios. Em caso de
        credenciais válidas, fecha a tela de login e dispara o callback
        ``on_login_success``; caso contrário, exibe uma mensagem de erro.
        """
        email = self.txt_email.get().strip()
        senha = self.txt_senha.get().strip()

        if not email or not senha:
            messagebox.showwarning(LocaleManager.t("titulo_erro"), LocaleManager.t("aviso"))
            return

        if self.controller.login(email, senha):
            self.destroy()           # Fecha a tela de login de forma limpa
            self.on_login_success()  # Dispara a abertura da MainWindow lá no main.py
        else:
            messagebox.showerror(LocaleManager.t("erro_acesso"), LocaleManager.t("msg_credenciais_incorretas"))