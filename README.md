# FitLogic - Gerador Inteligente de Treinos

> **Projeto prático desenvolvido para a disciplina de Laboratório de Desenvolvimento de Sistemas - IFSC**

---

### Modelagem UML inicial do projeto:
![UML](./images/UML%20do%20projeto.png)

---

## 🏋️‍♂️ O que é o FitLogic?

O **FitLogic** é uma aplicação desktop desenvolvida para automatizar e personalizar a prescrição de treinos de musculação. Através de uma interface gráfica moderna, o sistema analisa o perfil antropométrico do usuário (peso, altura, sexo), seu objetivo principal e seu biotipo fisionômico (Ectomorfo, Mesomorfo ou Endomorfo) para gerar uma ficha de treino periodizada e otimizada de forma 100% automatizada.

O principal diferencial do software é ir além do gerenciamento básico (CRUD), aplicando regras de negócio de educação física para calcular o volume semanal ideal de séries, repetições e o tempo de descanso adequado para cada tipo de corpo.

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Interface Gráfica (GUI):** CustomTkinter (Layout responsivo com suporte nativo a Dark/Light mode)
* **Banco de Dados & ORM:** SQLite + SQLAlchemy
* **Geração de Relatórios:** ReportLab (Geração de PDFs offline)
* **Internacionalização (i18n):** Biblioteca nativa `locale` + `gettext`
* **Documentação da API:** MkDocs (Docstrings no padrão Google)

---

## Como Instalar e Executar

### Pré-requisitos
Antes de começar, certifique-se de ter o **Python 3.10 ou superior** instalado em sua máquina.

### Passo a Passo

1. **Clone o repositório:**
```bash
   git clone [https://github.com/seu-usuario/Projeto-Python-Gerador-de-Treinos.git](https://github.com/seu-usuario/Projeto-Python-Gerador-de-Treinos.git)
   cd Projeto-Python-Gerador-de-Treinos

   # No Linux/macOS:
   python3 -m venv venv
   source venv/bin/activate

   # No Windows (Prompt de Comando):
   python -m venv venv
   venv\Scripts\activate

   # Instale as dependências
   pip install -r requirements.txt

   #Execute a aplicação:
   python main.py
```

---


## Funcionalidades Implementadas
* **Interface Gráfica Consistente:** Telas padronizadas usando CustomTkinter, com menus de navegação intuitivos e suporte total a teclas de atalho no teclado para acessibilidade.

* **Módulo de Cadastro Completo (CRUD):** Gerenciamento e persistência relacional de Usuários, Exercícios e Planos de Treino utilizando o ORM SQLAlchemy.

* **Algoritmo de Sugestão Inteligente:** Motor de regras que processa os dados biológicos do usuário e monta automaticamente a divisão do treino (ex: ABC, ABCD), distribuindo os exercícios e calculando volume de séries e descanso ideais.

* **Ficha de Treino em PDF:** Exportação da sugestão de treino gerada para um documento PDF profissional através da biblioteca ReportLab, pronto para impressão ou uso no celular.

---

## ToDo
* **Internacionalização Automática (i18n):** O sistema detecta o idioma padrão do Sistema Operacional do usuário no momento da inicialização e traduz toda a interface para Português, Inglês ou Espanhol de forma transparente, sem exigir configuração manual.
