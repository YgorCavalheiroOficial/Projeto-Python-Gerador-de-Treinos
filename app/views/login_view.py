import customtkinter as ctk
from tkinter import messagebox
from app.controllers.auth_controller import AuthController
from app.models.session_manager import SessionManager
from app.services.locale_manager import LocaleManager

class LoginView(ctk.CTk):
    def __init__(self, on_login_success, **kwargs):
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