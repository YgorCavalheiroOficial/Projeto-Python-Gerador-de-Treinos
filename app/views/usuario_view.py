import customtkinter as ctk
from tkinter import messagebox
from app.controllers.usuario_controller import UsuarioController
from app.views.components.custom_inputs import CustomFormInput
from app.services.locale_manager import LocaleManager  # Importação do gerenciador i18n

class UsuarioView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = UsuarioController()
        self.id_em_edicao = None 
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Formulário Lateral Esquerdo
        form_frame = ctk.CTkFrame(self, corner_radius=12)
        form_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        # Título do Formulário Traduzido
        self.lbl_titulo_form = ctk.CTkLabel(
            form_frame, 
            text=LocaleManager.t("titulo_usuarios"), 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.lbl_titulo_form.pack(pady=10)

        # Inputs Customizados Traduzidos
        self.txt_nome = CustomFormInput(form_frame, LocaleManager.t("lbl_nome"))
        self.txt_nome.pack(fill="x", padx=15, pady=4)

        self.txt_peso = CustomFormInput(form_frame, LocaleManager.t("lbl_peso"), "Ex: 75.5")
        self.txt_peso.pack(fill="x", padx=15, pady=4)

        self.txt_altura = CustomFormInput(form_frame, LocaleManager.t("lbl_altura"), "Ex: 1.78")
        self.txt_altura.pack(fill="x", padx=15, pady=4)

        # ComboBox de Sexo Traduzido
        ctk.CTkLabel(form_frame, text=LocaleManager.t("lbl_sexo"), font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=15, pady=(4,0))
        self.cb_sexo = ctk.CTkComboBox(
            form_frame, 
            values=[LocaleManager.t("sexo_m"), LocaleManager.t("sexo_f"), LocaleManager.t("sexo_ni")], 
            height=35
        )
        self.cb_sexo.pack(fill="x", padx=15, pady=4)
        
        # ComboBox de Biotipo Traduzido
        ctk.CTkLabel(form_frame, text=LocaleManager.t("lbl_biotipo"), font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=15, pady=(4,0))
        self.cb_biotipo = ctk.CTkComboBox(
            form_frame, 
            values=[LocaleManager.t("bio_ecto"), LocaleManager.t("bio_meso"), LocaleManager.t("bio_endo")], 
            height=35
        )
        self.cb_biotipo.pack(fill="x", padx=15, pady=4)

        # ComboBox de Objetivo Traduzido
        ctk.CTkLabel(form_frame, text=LocaleManager.t("lbl_objetivo"), font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=15, pady=(4,0))
        self.cb_objetivo = ctk.CTkComboBox(
            form_frame, 
            values=[LocaleManager.t("obj_hiper"), LocaleManager.t("obj_emag"), LocaleManager.t("obj_res")], 
            height=35
        )
        self.cb_objetivo.pack(fill="x", padx=15, pady=4)

        # Campo de Descrição Traduzido
        self.txt_descricao = CustomFormInput(form_frame, LocaleManager.t("lbl_descricao"), LocaleManager.t("ph_descricao"))
        self.txt_descricao.pack(fill="x", padx=15, pady=4)

        # Botões Principais Traduzidos
        self.btn_salvar = ctk.CTkButton(
            form_frame, 
            text=LocaleManager.t("btn_salvar_usuario"), 
            command=self.processar_salvamento, 
            fg_color="#2E7D32", 
            hover_color="#1B5E20", 
            height=38
        )
        self.btn_salvar.pack(fill="x", padx=15, pady=(15, 5))

        self.btn_cancelar = ctk.CTkButton(
            form_frame, 
            text=LocaleManager.t("btn_cancelar_edicao"), 
            command=self.limpar_formulario, 
            fg_color="#37474F", 
            hover_color="#263238", 
            height=30
        )

        # Divisor
        ctk.CTkLabel(form_frame, text="───────────────────────────").pack(pady=5)

        # Painel de Controle de Modificação/Exclusão
        action_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=5)

        self.txt_id_acao = ctk.CTkEntry(action_frame, placeholder_text="ID", width=60, height=35)
        self.txt_id_acao.pack(side="left", padx=(0, 5))

        btn_editar = ctk.CTkButton(
            action_frame, 
            text=LocaleManager.t("btn_editar"), 
            command=self.carregar_para_edicao, 
            width=80, 
            height=35, 
            fg_color="#1565C0", 
            hover_color="#0D47A1"
        )
        btn_editar.pack(side="left", padx=2)

        btn_excluir = ctk.CTkButton(
            action_frame, 
            text=LocaleManager.t("btn_excluir"), 
            command=self.excluir_registro, 
            width=80, 
            height=35, 
            fg_color="#C62828", 
            hover_color="#B71C1C"
        )
        btn_excluir.pack(side="left", padx=2)

        # Painel de Listagem Direito Traduzido
        list_frame = ctk.CTkFrame(self, corner_radius=12)
        list_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        
        ctk.CTkLabel(
            list_frame, 
            text=LocaleManager.t("titulo_lista_usuarios"), 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.lbl_titulo_lista = ctk.CTkLabel(list_frame, text=LocaleManager.t("titulo_lista_usuarios"), font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_titulo_lista.pack(pady=10)
        
        self.textbox = ctk.CTkTextbox(list_frame, font=ctk.CTkFont(family="Courier", size=12))
        self.textbox.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.atualizar_lista()

    def processar_salvamento(self):
        try:
            if self.id_em_edicao:
                # Operação de UPDATE
                self.controller.atualizar(
                    usuario_id=self.id_em_edicao,
                    nome=self.txt_nome.get(),
                    peso=self.txt_peso.get(),
                    altura=self.txt_altura.get(),
                    sexo=self.cb_sexo.get(),
                    biotipo=self.cb_biotipo.get(),
                    objetivo=self.cb_objetivo.get(),
                    descricao=self.txt_descricao.get()
                )
                messagebox.showinfo(LocaleManager.t("sucesso"), LocaleManager.t("msg_usuario_atualizado"))
            else:
                # Operação de CREATE
                self.controller.cadastrar(
                    nome=self.txt_nome.get(),
                    peso=self.txt_peso.get(),
                    altura=self.txt_altura.get(),
                    sexo=self.cb_sexo.get(),
                    biotipo=self.cb_biotipo.get(),
                    objetivo=self.cb_objetivo.get(),
                    descricao=self.txt_descricao.get()
                )
                messagebox.showinfo(LocaleManager.t("sucesso"), LocaleManager.t("msg_usuario_cadastrado"))
            
            self.limpar_formulario()
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror(LocaleManager.t("erro"), f"{LocaleManager.t('erro')}: {str(e)}")

    def carregar_para_edicao(self):
        id_busca = self.txt_id_acao.get()
        if not id_busca:
            messagebox.showwarning(LocaleManager.t("aviso"), LocaleManager.t("msg_informe_id_editar"))
            return
        
        usuario = self.controller.buscar_por_id(int(id_busca))
        if not usuario:
            messagebox.showerror(LocaleManager.t("erro"), LocaleManager.t("msg_usuario_nao_encontrado"))
            return

        # Ativa o modo de edição na interface gráfica com textos traduzidos dinamicamente
        self.id_em_edicao = usuario.id
        texto_edicao = f"{LocaleManager.t('titulo_editando')} (ID: {usuario.id})"
        self.lbl_titulo_form.configure(text=texto_edicao, text_color="#1E88E5")
        self.btn_salvar.configure(text=LocaleManager.t("btn_atualizar_dados"), fg_color="#1E88E5", hover_color="#1565C0")
        self.btn_cancelar.pack(fill="x", padx=15, pady=2)

        # Preenche os campos
        self.txt_nome.set_text(usuario.nome)
        self.txt_peso.set_text(usuario.peso)
        self.txt_altura.set_text(usuario.altura)
        self.cb_sexo.set(usuario.sexo)
        self.cb_biotipo.set(usuario.biotipo)
        self.cb_objetivo.set(usuario.objetivo)
        if usuario.descricao:
            self.txt_descricao.set_text(usuario.descricao)

    def excluir_registro(self):
        id_busca = self.txt_id_acao.get()
        if not id_busca:
            messagebox.showwarning(LocaleManager.t("aviso"), LocaleManager.t("msg_informe_id_excluir"))
            return
        
        pergunta = LocaleManager.t("msg_confirmar_exclusao").format(id_busca)
        if messagebox.askyesno(LocaleManager.t("confirmar"), pergunta):
            if self.controller.deletar(int(id_busca)):
                messagebox.showinfo(LocaleManager.t("sucesso"), LocaleManager.t("msg_registro_removido"))
                if self.id_em_edicao == int(id_busca):
                    self.limpar_formulario()
                self.txt_id_acao.delete(0, "end")
                self.atualizar_lista()
            else:
                messagebox.showerror(LocaleManager.t("erro"), LocaleManager.t("msg_id_nao_localizado"))

    def limpar_formulario(self):
        self.id_em_edicao = None
        self.lbl_titulo_form.configure(text=LocaleManager.t("titulo_usuarios"), text_color=["#000", "#fff"])
        self.btn_salvar.configure(text=LocaleManager.t("btn_salvar_usuario"), fg_color="#2E7D32", hover_color="#1B5E20")
        self.btn_cancelar.pack_forget()
        self.txt_nome.clear()
        self.txt_peso.clear()
        self.txt_altura.clear()
        self.txt_descricao.clear()

    def atualizar_lista(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        usuarios = self.controller.listar_todos()
        
        # Cabeçalhos da tabela traduzidos de forma tabular
        hdr_id = LocaleManager.t("hdr_id")
        hdr_nome = LocaleManager.t("hdr_nome")
        hdr_biotipo = LocaleManager.t("hdr_biotipo")
        hdr_imc = LocaleManager.t("hdr_imc")
        
        header = f"{hdr_id:<4} | {hdr_nome:<20} | {hdr_biotipo:<12} | {hdr_imc:<6}\n" + "-"*50 + "\n"
        self.textbox.insert("end", header)
        
        for u in usuarios:
            linha = f"{u.id:<4} | {u.nome[:20]:<20} | {u.biotipo:<12} | {u.calcular_imc():<6}\n"
            self.textbox.insert("end", linha)
        self.textbox.configure(state="disabled")