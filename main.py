from app.config import inicializar_banco
from app.services.locale_manager import LocaleManager
from app.views.main_window import MainWindow

def main():
    LocaleManager.inicializar()

    print("[FitLogic] Inicializando persistência relacional (SQLite + SQLAlchemy)...")
    inicializar_banco()
    
    print("[FitLogic] Renderizando interface desktop...")
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()