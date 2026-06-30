# FitLogic — Documentação da API

Esta documentação é gerada **automaticamente** a partir dos docstrings
(comentários de documentação) presentes diretamente no código-fonte
Python, no padrão Google Style — equivalente ao Javadoc para projetos Java.

Para gerar/atualizar esta documentação localmente, execute na raiz do projeto:

```bash
pip install mkdocs mkdocs-material "mkdocstrings[python]"
mkdocs serve   # visualizar em http://127.0.0.1:8000
mkdocs build   # gerar a versão estática em site/
```

## Arquitetura do projeto

O FitLogic segue o padrão **MVC (Model-View-Controller)**:

- **Models** (`app/models`): entidades de domínio mapeadas via SQLAlchemy ORM (Usuario, Exercicio, PlanoTreino, ItemTreino, Professor, SessionManager).
- **Controllers** (`app/controllers`): orquestram a comunicação entre as views e os models/services.
- **Services** (`app/services`): regras de negócio reutilizáveis (algoritmo de geração de treino, exportação em PDF, internacionalização).
- **Views** (`app/views`): interface gráfica construída com CustomTkinter.

Use o menu lateral para navegar entre os módulos documentados.
