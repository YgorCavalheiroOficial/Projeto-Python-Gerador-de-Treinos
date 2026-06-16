from app.config import inicializar_banco
from app.views.main_window import MainWindow

def main():
    print("[FitLogic] Inicializando persistência relacional (SQLite + SQLAlchemy)...")
    inicializar_banco()
    
    print("[FitLogic] Renderizando interface desktop...")
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()