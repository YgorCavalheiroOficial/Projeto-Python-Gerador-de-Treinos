"""Componentes de formulário reutilizáveis para as telas do FitLogic."""

import customtkinter as ctk

class CustomFormInput(ctk.CTkFrame):
    """Campo de formulário padronizado (rótulo + caixa de texto).

    Garante a consistência visual exigida entre todas as telas do sistema,
    evitando a repetição de configuração de rótulo/entrada em cada view.

    Attributes:
        label (ctk.CTkLabel): Rótulo exibido acima do campo.
        entry (ctk.CTkEntry): Caixa de texto onde o usuário digita o valor.
    """

    def __init__(self, master, label_text, placeholder="", **kwargs):
        """Inicializa o componente de campo de formulário.

        Args:
            master: Widget pai (container) onde este componente será
                renderizado.
            label_text (str): Texto do rótulo exibido acima do campo.
            placeholder (str, optional): Texto de exemplo exibido quando o
                campo está vazio. Padrão: ``""``.
            **kwargs: Argumentos adicionais repassados ao ``ctk.CTkFrame``.
        """
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.label = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(size=13, weight="bold"))
        self.label.pack(anchor="w", pady=(0, 2))
        
        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder, height=35, corner_radius=8)
        self.entry.pack(fill="x", expand=True)

    def get(self):
        """Retorna o valor atualmente digitado no campo.

        Returns:
            str: Texto contido na caixa de entrada.
        """
        return self.entry.get()

    def clear(self):
        """Limpa o conteúdo do campo de entrada."""
        self.entry.delete(0, "end")

    def set_text(self, text):
        """Preenche o campo com um texto específico (Útil para Edição).

        Args:
            text: Valor a ser inserido no campo (convertido para string).
        """
        self.clear()
        self.entry.insert(0, str(text))