"""Tela de geração e exportação de planos de treino."""

import customtkinter as ctk
import os
from tkinter import messagebox, filedialog
from app.controllers.treino_controller import TreinoController
from app.controllers.usuario_controller import UsuarioController
from app.services.locale_manager import LocaleManager 

class TreinoView(ctk.CTkFrame):
    """Tela responsável pela geração inteligente e exportação de treinos.

    Permite ao professor selecionar um aluno já cadastrado, disparar o
    algoritmo de prescrição automática
    (:class:`~app.controllers.treino_controller.TreinoController`) e
    exportar o resultado em PDF, representando a funcionalidade central do
    sistema (vai além do CRUD).

    Attributes:
        treino_controller (TreinoController): Controller de geração/exportação de treinos.
        usuario_controller (UsuarioController): Controller usado para listar os alunos disponíveis.
        plano_atual (PlanoTreino | None): Último plano de treino gerado nesta sessão de tela.
    """

    def __init__(self, master, **kwargs):
        """Inicializa a view, instanciando os controllers e montando a interface.

        Args:
            master: Widget pai (container) onde esta tela será renderizada.
            **kwargs: Argumentos adicionais repassados ao ``ctk.CTkFrame``.
        """
        super().__init__(master, **kwargs)
        self.treino_controller = TreinoController()
        self.usuario_controller = UsuarioController()
        self.plano_atual = None
        self.setup_ui()

    def setup_ui(self):
        """Monta os widgets da tela: seleção de aluno, área de resultado e exportação."""
        self.grid_columnconfigure(0, weight=1)

        # Top Bar para seleção de Aluno
        top_frame = ctk.CTkFrame(self, height=70, corner_radius=12)
        top_frame.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(top_frame, text=LocaleManager.t("selecione_aluno"), font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=15)
        
        self.cb_usuarios = ctk.CTkComboBox(top_frame, values=[], width=250, height=35)
        self.cb_usuarios.pack(side="left", padx=10)
        
        self.btn_carregar = ctk.CTkButton(top_frame, text=LocaleManager.t("sincronizar_alunos"), command=self.carregar_usuarios, width=150, height=35)
        self.btn_carregar.pack(side="left", padx=5)

        self.btn_gerar = ctk.CTkButton(top_frame, text=LocaleManager.t("gerar_treino_inteligente"), command=self.gerar_treino, fg_color="#E65100", hover_color="#BF360C", height=35)
        self.btn_gerar.pack(side="left", padx=10)

        # Conteúdo do Treino
        self.content_frame = ctk.CTkFrame(self, corner_radius=12)
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.txt_treino = ctk.CTkTextbox(self.content_frame, font=ctk.CTkFont(family="Courier", size=12))
        self.txt_treino.pack(fill="both", expand=True, padx=20, pady=20)

        self.btn_pdf = ctk.CTkButton(self, text=LocaleManager.t("exportar_ficha_treino"), command=self.exportar_pdf, state="disabled", fg_color="#1565C0", height=45)
        self.btn_pdf.pack(fill="x", padx=15, pady=(0, 15))

        self.carregar_usuarios()

    def carregar_usuarios(self):
        """Atualiza o combobox de seleção com a lista de alunos do professor logado.

        Consulta os alunos via :class:`UsuarioController`, monta um mapa
        ``"id - nome" -> id`` para facilitar a seleção e pré-seleciona o
        primeiro aluno da lista, caso exista.
        """
        usuarios = self.usuario_controller.listar_todos()
        self.mapeamento_usuarios = {f"{u.id} - {u.nome}": u.id for u in usuarios}
        self.cb_usuarios.configure(values=list(self.mapeamento_usuarios.keys()))
        if self.mapeamento_usuarios:
            self.cb_usuarios.set(list(self.mapeamento_usuarios.keys())[0])

    def gerar_treino(self):
        """Aciona a geração de um novo plano de treino para o aluno selecionado.

        Valida se um aluno foi selecionado, solicita ao
        :class:`TreinoController` a geração do plano e exibe o resultado
        formatado na área de texto, habilitando o botão de exportação em
        PDF ao final.
        """
        selecionado = self.cb_usuarios.get()
        if not selecionado:
            messagebox.showwarning(LocaleManager.t("titulo_erro"), LocaleManager.t("erro_selecionar_usuario"))
            return

        usuario_id = self.mapeamento_usuarios[selecionado]
        self.plano_atual = self.treino_controller.gerar_novo_treino(usuario_id)

        if self.plano_atual:
            self.txt_treino.delete("0.0", "end")
            resumo = f"PLANO DE TREINO GERADO COM SUCESSO\n"
            resumo += f"Estrutura de Divisão: {self.plano_atual.divisao_treino}\n"
            resumo += f"="*60 + "\n"
            
            for item in self.plano_atual.itens:
                resumo += f"-> {item.exercicio.nome:<22} | {item.series}x{item.repeticoes:<2} | Descanso: {item.descanso_segundos}s\n"
            
            self.txt_treino.insert("end", resumo)
            self.btn_pdf.configure(state="normal")
            messagebox.showinfo(LocaleManager.t("titulo_sucesso"), LocaleManager.t("treino_gerado_sucesso"))

    def exportar_pdf(self):
        """Exporta o plano de treino atualmente exibido para um arquivo PDF.

        Abre uma caixa de diálogo nativa para o usuário escolher o local de
        salvamento e delega a geração do arquivo ao
        :class:`TreinoController`, exibindo uma confirmação ao final.
        """
        if not self.plano_atual:
            return
        
        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[(LocaleManager.t("documentos_pdf"), "*.pdf")],
            title=LocaleManager.t("salvar_ficha_treino")
        )
        
        if caminho:
            self.treino_controller.baixar_pdf(self.plano_atual.id, caminho)
            msg_sucesso = f"{LocaleManager.t('pdf_salvo_sucesso')}\n{caminho}"
            messagebox.showinfo(LocaleManager.t("titulo_sucesso"), msg_sucesso)