"""Tela de cadastro e gerenciamento do catálogo de exercícios."""

import customtkinter as ctk
from tkinter import messagebox
from app.controllers.exercicio_controller import ExercicioController
from app.views.components.custom_inputs import CustomFormInput
from app.services.locale_manager import LocaleManager 

class ExercicioView(ctk.CTkFrame):
    """Tela de CRUD do catálogo de exercícios, com formulário e listagem.

    Segue o mesmo padrão visual e de organização de botões das demais
    telas do sistema (formulário à esquerda, listagem à direita, ações de
    editar/excluir por ID), garantindo a consistência exigida entre as
    telas da aplicação.

    Attributes:
        controller (ExercicioController): Controller responsável pelas
            operações de CRUD de exercícios.
        id_em_edicao (int | None): Identificador do exercício atualmente em
            edição, ou ``None`` quando o formulário está em modo de
            cadastro (novo registro).
    """

    def __init__(self, master, **kwargs):
        """Inicializa a view, instanciando o controller e montando a interface.

        Args:
            master: Widget pai (container) onde esta tela será renderizada.
            **kwargs: Argumentos adicionais repassados ao ``ctk.CTkFrame``.
        """
        super().__init__(master, **kwargs)
        self.controller = ExercicioController()
        self.id_em_edicao = None
        self.setup_ui()

    def setup_ui(self):
        """Monta os widgets da tela: formulário de cadastro/edição e listagem."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Form lateral
        form_frame = ctk.CTkFrame(self, corner_radius=12)
        form_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.lbl_titulo_form = ctk.CTkLabel(form_frame, text=LocaleManager.t("titulo_exercicios"), font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_titulo_form.pack(pady=10)

        self.txt_nome = CustomFormInput(form_frame, LocaleManager.t("lbl_nome_exercicio"))
        self.txt_nome.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(form_frame, text=LocaleManager.t("lbl_grupo_muscular"), font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=15, pady=(5,0))
        self.cb_grupo = ctk.CTkComboBox(form_frame, values = [
                                                        LocaleManager.t("chest"), 
                                                        LocaleManager.t("back"), 
                                                        LocaleManager.t("quadriceps"), 
                                                        LocaleManager.t("hamstrings"), 
                                                        LocaleManager.t("calves"), 
                                                        LocaleManager.t("biceps"), 
                                                        LocaleManager.t("triceps"), 
                                                        LocaleManager.t("forearms"), 
                                                        LocaleManager.t("shoulders"), 
                                                        LocaleManager.t("cardio")
                                                    ], height=35)
        
        self.cb_grupo.pack(fill="x", padx=15, pady=5)

        self.txt_desc = CustomFormInput(form_frame, LocaleManager.t("lbl_breve_descricao"), LocaleManager.t("pe_descricao"))
        self.txt_desc.pack(fill="x", padx=15, pady=5)

        self.btn_salvar = ctk.CTkButton(form_frame, text=LocaleManager.t("btn_salvar_exercicio"), command=self.processar_salvamento, fg_color="#2E7D32", hover_color="#1B5E20", height=40)
        self.btn_salvar.pack(fill="x", padx=15, pady=(15, 5))

        self.btn_cancelar = ctk.CTkButton(form_frame, text=LocaleManager.t("cancelar"), command=self.limpar_formulario, fg_color="#37474F", hover_color="#263238", height=30)

        ctk.CTkLabel(form_frame, text="───────────────────────────").pack(pady=5)

        # Painel de Modificação por ID
        action_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=5)

        self.txt_id_acao = ctk.CTkEntry(action_frame, placeholder_text="ID", width=60, height=35)
        self.txt_id_acao.pack(side="left", padx=(0, 5))

        btn_editar = ctk.CTkButton(action_frame, text=LocaleManager.t("btn_editar"), command=self.carregar_para_edicao, width=80, height=35, fg_color="#1565C0", hover_color="#0D47A1")
        btn_editar.pack(side="left", padx=2)

        btn_excluir = ctk.CTkButton(action_frame, text=LocaleManager.t("btn_excluir"), command=self.excluir_registro, width=80, height=35, fg_color="#C62828", hover_color="#B71C1C")
        btn_excluir.pack(side="left", padx=2)

        # Painel direito
        list_frame = ctk.CTkFrame(self, corner_radius=12)
        list_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(list_frame, text=LocaleManager.t("titulo_catalogo"), font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        self.textbox = ctk.CTkTextbox(list_frame, font=ctk.CTkFont(family="Courier", size=12))
        self.textbox.pack(fill="both", expand=True, padx=15, pady=15)

        self.atualizar_lista()

    def processar_salvamento(self):
        """Cadastra um novo exercício ou atualiza um existente.

        Valida se o campo de nome foi preenchido. Quando
        :attr:`id_em_edicao` está definido, delega a atualização ao
        controller; caso contrário, cadastra um novo exercício. Ao final,
        limpa o formulário e atualiza a listagem.
        """
        if not self.txt_nome.get():
            messagebox.showwarning(LocaleManager.t("titulo_erro"), LocaleManager.t("aviso"))
            return
        
        if self.id_em_edicao:
            self.controller.atualizar(exercicio_id=self.id_em_edicao, nome=self.txt_nome.get(), grupo_muscular=self.cb_grupo.get(), descricao=self.txt_desc.get())
            messagebox.showinfo(LocaleManager.t("titulo_sucesso"), LocaleManager.t("msg_exercicio_atualizado"))
        else:
            self.controller.cadastrar(nome=self.txt_nome.get(), grupo_muscular=self.cb_grupo.get(), descricao=self.txt_desc.get())
            messagebox.showinfo(LocaleManager.t("titulo_sucesso"), LocaleManager.t("msg_exercicio_cadastrado"))
            
        self.limpar_formulario()
        self.atualizar_lista()

    def carregar_para_edicao(self):
        """Carrega os dados de um exercício (pelo ID informado) no formulário.

        Busca o exercício pelo ID digitado no campo de ações e, se
        encontrado, preenche o formulário com seus dados, alternando a
        tela para o modo de edição (:attr:`id_em_edicao` definido).
        """
        id_busca = self.txt_id_acao.get()
        if not id_busca:
            messagebox.showwarning(LocaleManager.t("titulo_erro"), LocaleManager.t("msg_id_nao_localizado"))
            return
        
        ex = self.controller.buscar_por_id(int(id_busca))
        if not ex:
            messagebox.showerror(LocaleManager.t("erro"), LocaleManager.t("msg_id_nao_localizado"))
            return

        self.id_em_edicao = ex.id
        
        texto_edicao = f"{LocaleManager.t('titulo_editando')} (ID: {ex.id})"
        self.lbl_titulo_form.configure(text=texto_edicao, text_color="#1E88E5")
        self.btn_salvar.configure(text=LocaleManager.t("btn_atualizar_dados"), fg_color="#1E88E5", hover_color="#1565C0")
        self.btn_cancelar.pack(fill="x", padx=15, pady=2)

        self.txt_nome.set_text(ex.nome)
        self.cb_grupo.set(ex.grupo_muscular)
        self.txt_desc.set_text(ex.descricao if ex.descricao else "")

    def excluir_registro(self):
        """Exclui o exercício correspondente ao ID informado, após confirmação.

        Solicita confirmação do usuário antes de remover o registro. Se o
        exercício excluído for o que estava em edição, o formulário é
        limpo automaticamente.
        """
        id_busca = self.txt_id_acao.get()
        if not id_busca:
            messagebox.showwarning(LocaleManager.t("titulo_erro"), LocaleManager.t("msg_id_nao_localizado"))
            return
        
        mensagem_confirmacao = LocaleManager.t("msg_confirmar_exclusao").format(id_busca)
        if messagebox.askyesno(LocaleManager.t("confirmar"), mensagem_confirmacao):
            if self.controller.deletar(int(id_busca)):
                messagebox.showinfo(LocaleManager.t("titulo_sucesso"), LocaleManager.t("msg_registro_removido"))
                if self.id_em_edicao == int(id_busca):
                    self.limpar_formulario()
                self.txt_id_acao.delete(0, "end")
                self.atualizar_lista()
            else:
                messagebox.showerror(LocaleManager.t("erro"), LocaleManager.t("erro"))

    def limpar_formulario(self):
        """Restaura o formulário ao estado inicial de cadastro (não edição)."""
        self.id_em_edicao = None
        self.lbl_titulo_form.configure(text=LocaleManager.t("titulo_exercicios"), text_color=("#000", "#fff"))
        self.btn_salvar.configure(text=LocaleManager.t("btn_salvar_exercicio"), fg_color="#2E7D32", hover_color="#1B5E20")
        self.btn_cancelar.pack_forget()
        self.txt_nome.clear()
        self.txt_desc.clear()

    def atualizar_lista(self):
        """Recarrega a listagem de exercícios cadastrados no catálogo.

        Limpa a área de texto e reconstrói a listagem tabular (ID, nome e
        grupo muscular) a partir dos dados atuais do banco de dados.
        """
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        exercicios = self.controller.listar_todos()

        header = f"{'ID':<4} | {LocaleManager.t('hdr_exercicio'):<25} | {LocaleManager.t('hdr_grupo'):<15}\n" + "-"*50 + "\n"
        self.textbox.insert("end", header)

        for ex in exercicios:
            linha = f"{ex.id:<4} | {ex.nome[:25]:<25} | {ex.grupo_muscular:<15}\n"
            self.textbox.insert("end", linha)
        self.textbox.configure(state="disabled")