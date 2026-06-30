import customtkinter as ctk
from tkinter import messagebox
from app.controllers.exercicio_controller import ExercicioController
from app.views.components.custom_inputs import CustomFormInput

class ExercicioView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = ExercicioController()
        self.id_em_edicao = None
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Form lateral
        form_frame = ctk.CTkFrame(self, corner_radius=12)
        form_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.lbl_titulo_form = ctk.CTkLabel(form_frame, text="Cadastro de Exercício", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_titulo_form.pack(pady=10)

        self.txt_nome = CustomFormInput(form_frame, "Nome do Exercício:")
        self.txt_nome.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(form_frame, text="Grupo Muscular:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=15, pady=(5,0))
        self.cb_grupo = ctk.CTkComboBox(form_frame, values=["Peito", "Costas", "Quadríceps", "Posterior", "Panturrilha", "Bíceps", "Tríceps", "Antebraço", "Ombros", "Cárdio"], height=35)
        # CORREÇÃO: Alterado de py=5 para pady=5
        self.cb_grupo.pack(fill="x", padx=15, pady=5)

        self.txt_desc = CustomFormInput(form_frame, "Breve Descrição:")
        # CORREÇÃO: Alterado de py=5 para pady=5
        self.txt_desc.pack(fill="x", padx=15, pady=5)

        self.btn_salvar = ctk.CTkButton(form_frame, text="Salvar Exercício", command=self.processar_salvamento, fg_color="#2E7D32", hover_color="#1B5E20", height=40)
        self.btn_salvar.pack(fill="x", padx=15, pady=(15, 5))

        self.btn_cancelar = ctk.CTkButton(form_frame, text="Cancelar Edição", command=self.limpar_formulario, fg_color="#37474F", hover_color="#263238", height=30)

        ctk.CTkLabel(form_frame, text="───────────────────────────").pack(pady=5)

        # Painel de Modificação por ID
        action_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=5)

        self.txt_id_acao = ctk.CTkEntry(action_frame, placeholder_text="ID", width=60, height=35)
        self.txt_id_acao.pack(side="left", padx=(0, 5))

        btn_editar = ctk.CTkButton(action_frame, text="✏️ Editar", command=self.carregar_para_edicao, width=80, height=35, fg_color="#1565C0", hover_color="#0D47A1")
        btn_editar.pack(side="left", padx=2)

        btn_excluir = ctk.CTkButton(action_frame, text="🗑️ Excluir", command=self.excluir_registro, width=80, height=35, fg_color="#C62828", hover_color="#B71C1C")
        btn_excluir.pack(side="left", padx=2)

        # Painel direito
        list_frame = ctk.CTkFrame(self, corner_radius=12)
        list_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(list_frame, text="Catálogo de Exercícios", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        self.textbox = ctk.CTkTextbox(list_frame, font=ctk.CTkFont(family="Courier", size=12))
        self.textbox.pack(fill="both", expand=True, padx=15, pady=15)

        self.atualizar_lista()

    def processar_salvamento(self):
        if not self.txt_nome.get():
            messagebox.showwarning("Aviso", "O nome do exercício é obrigatório.")
            return
        
        if self.id_em_edicao:
            self.controller.atualizar(exercicio_id=self.id_em_edicao, nome=self.txt_nome.get(), grupo_muscular=self.cb_grupo.get(), descricao=self.txt_desc.get())
            messagebox.showinfo("Sucesso", "Exercício modificado com sucesso!")
        else:
            self.controller.cadastrar(nome=self.txt_nome.get(), grupo_muscular=self.cb_grupo.get(), descricao=self.txt_desc.get())
            messagebox.showinfo("Sucesso", "Exercício adicionado ao catálogo!")
            
        self.limpar_formulario()
        self.atualizar_lista()

    def carregar_para_edicao(self):
        id_busca = self.txt_id_acao.get()
        if not id_busca:
            messagebox.showwarning("Aviso", "Digite o ID do exercício.")
            return
        
        ex = self.controller.buscar_por_id(int(id_busca))
        if not ex:
            messagebox.showerror("Erro", "Exercício inexistente.")
            return

        self.id_em_edicao = ex.id
        self.lbl_titulo_form.configure(text=f"Editando Exercício (ID: {ex.id})", text_color="#1E88E5")
        self.btn_salvar.configure(text="Atualizar Dados", fg_color="#1E88E5", hover_color="#1565C0")
        self.btn_cancelar.pack(fill="x", padx=15, pady=2)

        self.txt_nome.set_text(ex.nome)
        self.cb_grupo.set(ex.grupo_muscular)
        self.txt_desc.set_text(ex.descricao if ex.descricao else "")

    def excluir_registro(self):
        id_busca = self.txt_id_acao.get()
        if not id_busca:
            messagebox.showwarning("Aviso", "Falta indicar o ID.")
            return
        
        if messagebox.askyesno("Confirmar", f"Apagar o exercício ID {id_busca} permanentemente?"):
            if self.controller.deletar(int(id_busca)):
                messagebox.showinfo("Sucesso", "Removido com sucesso.")
                if self.id_em_edicao == int(id_busca):
                    self.limpar_formulario()
                self.txt_id_acao.delete(0, "end")
                self.atualizar_lista()
            else:
                messagebox.showerror("Erro", "Não encontrado.")

    def limpar_formulario(self):
        self.id_em_edicao = None
        # CORREÇÃO PREVENTIVA: Trocado colchetes [] por parênteses ()
        self.lbl_titulo_form.configure(text="Cadastro de Exercício", text_color=("#000", "#fff"))
        self.btn_salvar.configure(text="Salvar Exercício", fg_color="#2E7D32", hover_color="#1B5E20")
        self.btn_cancelar.pack_forget()
        self.txt_nome.clear()
        self.txt_desc.clear()

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