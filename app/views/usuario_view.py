import customtkinter as ctk
from tkinter import messagebox
from app.controllers.usuario_controller import UsuarioController
from app.views.components.custom_inputs import CustomFormInput

class UsuarioView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = UsuarioController()
        self.setup_ui()

    def setup_ui(self):
        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Formulário Lateral Esquerdo
        form_frame = ctk.CTkFrame(self, corner_radius=12)
        form_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(form_frame, text="Cadastro de Usuário", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        self.txt_nome = CustomFormInput(form_frame, "Nome Completo:")
        self.txt_nome.pack(fill="x", padx=15, pady=5)

        self.txt_peso = CustomFormInput(form_frame, "Peso (kg):", "Ex: 75.5")
        self.txt_peso.pack(fill="x", padx=15, pady=5)

        self.txt_altura = CustomFormInput(form_frame, "Altura (m):", "Ex: 1.78")
        self.txt_altura.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(form_frame, text="Biotipo:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=15, pady=(5,0))
        self.cb_biotipo = ctk.CTkComboBox(form_frame, values=["Ectomorfo", "Mesomorfo", "Endomorfo"], height=35)
        self.cb_biotipo.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(form_frame, text="Objetivo:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=15, pady=(5,0))
        self.cb_objetivo = ctk.CTkComboBox(form_frame, values=["Hipertrofia", "Emagrecimento", "Resistência"], height=35)
        self.cb_objetivo.pack(fill="x", padx=15, pady=5)

        self.btn_salvar = ctk.CTkButton(form_frame, text="Salvar Usuário", command=self.salvar_usuario, fg_color="#2E7D32", hover_color="#1B5E20", height=40)
        self.btn_salvar.pack(fill="x", padx=15, pady=20)

        # Painel de Listagem Direito
        list_frame = ctk.CTkFrame(self, corner_radius=12)
        list_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        
        ctk.CTkLabel(list_frame, text="Usuários Cadastrados", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(list_frame, font=ctk.CTkFont(family="Courier", size=12))
        self.textbox.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.atualizar_lista()

    def salvar_usuario(self):
        try:
            self.controller.cadastrar(
                nome=self.txt_nome.get(),
                peso=self.txt_peso.get(),
                altura=self.txt_altura.get(),
                sexo="Masculino",
                biotipo=self.cb_biotipo.get(),
                objetivo=self.cb_objetivo.get()
            )
            messagebox.showinfo("Sucesso", "Usuário cadastrado perfeitamente!")
            self.txt_nome.clear()
            self.txt_peso.clear()
            self.txt_altura.clear()
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {str(e)}")

    def atualizar_lista(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        usuarios = self.controller.listar_todos()
        
        header = f"{'ID':<4} | {'Nome':<20} | {'Biotipo':<12} | {'IMC':<6}\n" + "-"*50 + "\n"
        self.textbox.insert("end", header)
        
        for u in usuarios:
            linha = f"{u.id:<4} | {u.nome[:20]:<20} | {u.biotipo:<12} | {u.calcular_imc():<6}\n"
            self.textbox.insert("end", linha)
        self.textbox.configure(state="disabled")