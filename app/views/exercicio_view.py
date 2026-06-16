import customtkinter as ctk
from tkinter import messagebox
from app.controllers.exercicio_controller import ExercicioController
from app.views.components.custom_inputs import CustomFormInput

class ExercicioView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = ExercicioController()
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Form lateral
        form_frame = ctk.CTkFrame(self, corner_radius=12)
        form_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(form_frame, text="Cadastro de Exercício", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        self.txt_nome = CustomFormInput(form_frame, "Nome do Exercício:")
        self.txt_nome.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(form_frame, text="Grupo Muscular:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=15, pady=(5,0))
        self.cb_grupo = ctk.CTkComboBox(form_frame, values=["Peito", "Costas", "Pernas", "Braços", "Ombros"], height=35)
        self.cb_grupo.pack(fill="x", padx=15, pady=5)

        self.txt_desc = CustomFormInput(form_frame, "Breve Descrição:")
        self.txt_desc.pack(fill="x", padx=15, pady=5)

        self.btn_salvar = ctk.CTkButton(form_frame, text="Salvar Exercício", command=self.salvar_exercicio, fg_color="#2E7D32", hover_color="#1B5E20", height=40)
        self.btn_salvar.pack(fill="x", padx=15, pady=20)

        # Painel direito
        list_frame = ctk.CTkFrame(self, corner_radius=12)
        list_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(list_frame, text="Catálogo de Exercícios", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        self.textbox = ctk.CTkTextbox(list_frame, font=ctk.CTkFont(family="Courier", size=12))
        self.textbox.pack(fill="both", expand=True, padx=15, pady=15)

        self.atualizar_lista()

    def salvar_exercicio(self):
        if not self.txt_nome.get():
            messagebox.showwarning("Aviso", "O nome do exercício é obrigatório.")
            return
        self.controller.cadastrar(nome=self.txt_nome.get(), grupo_muscular=self.cb_grupo.get(), descricao=self.txt_desc.get())
        messagebox.showinfo("Sucesso", "Exercício adicionado!")
        self.txt_nome.clear()
        self.txt_desc.clear()
        self.atualizar_lista()

    def atualizar_lista(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        exercicios = self.controller.listar_todos()

        header = f"{'ID':<4} | {'Exercício':<25} | {'Grupo Muscular':<15}\n" + "-"*50 + "\n"
        self.textbox.insert("end", header)

        for ex in exercicios:
            linha = f"{ex.id:<4} | {ex.nome[:25]:<25} | {ex.grupo_muscular:<15}\n"
            self.textbox.insert("end", linha)
        self.textbox.configure(state="disabled")