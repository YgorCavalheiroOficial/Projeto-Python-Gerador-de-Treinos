import customtkinter as ctk
import os
from tkinter import messagebox, filedialog
from app.controllers.treino_controller import TreinoController
from app.controllers.usuario_controller import UsuarioController

class TreinoView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.treino_controller = TreinoController()
        self.usuario_controller = UsuarioController()
        self.plano_atual = None
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Top Bar para seleção de Aluno
        top_frame = ctk.CTkFrame(self, height=70, corner_radius=12)
        top_frame.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(top_frame, text="Selecione o Aluno:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=15)
        
        self.cb_usuarios = ctk.CTkComboBox(top_frame, values=[], width=250, height=35)
        self.cb_usuarios.pack(side="left", padx=10)
        
        self.btn_carregar = ctk.CTkButton(top_frame, text="🔄 Sincronizar Alunos", command=self.carregar_usuarios, width=150, height=35)
        self.btn_carregar.pack(side="left", padx=5)

        self.btn_gerar = ctk.CTkButton(top_frame, text="⚡ Gerar Treino Inteligente", command=self.gerar_treino, fg_color="#E65100", hover_color="#BF360C", height=35)
        self.btn_gerar.pack(side="left", padx=10)

        # Conteúdo do Treino
        self.content_frame = ctk.CTkFrame(self, corner_radius=12)
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.txt_treino = ctk.CTkTextbox(self.content_frame, font=ctk.CTkFont(family="Courier", size=12))
        self.txt_treino.pack(fill="both", expand=True, padx=20, pady=20)

        self.btn_pdf = ctk.CTkButton(self, text="💾 Exportar Ficha de Treino Oficial (PDF)", command=self.exportar_pdf, state="disabled", fg_color="#1565C0", height=45)
        self.btn_pdf.pack(fill="x", padx=15, pady=(0, 15))

        self.carregar_usuarios()

    def carregar_usuarios(self):
        usuarios = self.usuario_controller.listar_todos()
        self.mapeamento_usuarios = {f"{u.id} - {u.nome}": u.id for u in usuarios}
        self.cb_usuarios.configure(values=list(self.mapeamento_usuarios.keys()))
        if self.mapeamento_usuarios:
            self.cb_usuarios.set(list(self.mapeamento_usuarios.keys())[0])

    def gerar_treino(self):
        selecionado = self.cb_usuarios.get()
        if not selecionado:
            messagebox.showwarning("Aviso", "Cadastre e selecione um aluno primeiro.")
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
            messagebox.showinfo("Motor Inteligente", "Regras aplicadas e treino estruturado com sucesso!")

    def exportar_pdf(self):
        if not self.plano_atual:
            return
        
        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Documentos PDF", "*.pdf")],
            title="Salvar Ficha de Treino"
        )
        
        if caminho:
            self.treino_controller.baixar_pdf(self.plano_atual.id, caminho)
            messagebox.showinfo("PDF Exportado", f"Ficha salva com sucesso em:\n{caminho}")