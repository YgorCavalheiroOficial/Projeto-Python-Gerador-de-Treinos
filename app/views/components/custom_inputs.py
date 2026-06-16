import customtkinter as ctk

class CustomFormInput(ctk.CTkFrame):
    """Componente reutilizável para manter consistência visual nos formulários."""
    def __init__(self, master, label_text, placeholder="", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.label = ctk.CTkLabel(self, text=label_text, font=ctk.CTkFont(size=13, weight="bold"))
        self.label.pack(anchor="w", pady=(0, 2))
        
        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder, height=35, corner_radius=8)
        self.entry.pack(fill="x", expand=True)

    def get(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, "end")