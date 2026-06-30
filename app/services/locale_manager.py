import locale
import os
import sys

class LocaleManager:
    # Idioma padrão caso a detecção falhe ou o idioma do SO não seja suportado
    _idioma_ativo = "pt"
    
    # Dicionário central de traduções para as três línguas exigidas
    _traducoes = {
        "pt": {
            "app_titulo": "FitLogic - Sistema Integrado de Prescrição",
            "btn_alunos": "Alunos (Ctrl+U)",
            "btn_exercicios": "Exercícios (Ctrl+E)",
            "btn_gerar_treinos": "Gerar Treinos (Ctrl+T)",

            "btn_nav_alunos": "Alunos (Ctrl+U)",
            "btn_nav_exercicios": "Exercícios (Ctrl+E)",
            "btn_nav_treinos": "Gerar Treinos (Ctrl+T)",
            
            # Tela de Usuários
            "titulo_usuarios": "Cadastro de Usuário",
            "lbl_nome": "Nome Completo:",
            "lbl_peso": "Peso (kg):",
            "lbl_altura": "Altura (m):",
            "lbl_biotipo": "Biotipo:",
            "lbl_objetivo": "Objetivo:",
            "btn_salvar_usuario": "Salvar Usuário",
            "btn_cancelar_edicao": "Cancelar Edição",
            "titulo_lista_usuarios": "Usuários Cadastrados",
            
            # Tela de Exercícios
            "titulo_exercicios": "Cadastro de Exercício",
            "lbl_nome_exercicio": "Nome do Exercício:",
            "lbl_grupo_muscular": "Grupo Muscular:",
            "lbl_breve_descricao": "Breve Descrição:",
            "lbl_descricao": "Breve Descrição:",
            "btn_salvar_exercicio": "Salvar Exercício",
            "titulo_catalogo": "Catálogo de Exercícios",
            "titulo_lista_exercicios": "Catálogo de Exercícios",
            "hdr_exercicio": "Exercício",
            "hdr_grupo": "Grupo Muscular",
            
            # Feedbacks e Mensagens
            "sucesso": "Sucesso",
            "erro": "Erro",
            "aviso": "Aviso",
            "msg_usuario_cadastrado": "Usuário cadastrado com sucesso!",
            "msg_usuario_atualizado": "Usuário atualizado com sucesso!",
            "msg_exercicio_cadastrado": "Exercício adicionado ao catálogo!",
            "msg_exercicio_atualizado": "Exercício modificado com sucesso!",
            "msg_confirmar_exclusao": "Tem certeza que deseja deletar o ID {} permanentemente?",

            # Chaves auxiliares que complementam o formulário
            "lbl_sexo": "Sexo:",
            "ph_descricao": "Descreva problemas de saúde ou desconfortos musculares...",
            "sexo_m": "Masculino", "sexo_f": "Feminino", "sexo_ni": "Prefiro não informar",
            "bio_ecto": "Ectomorfo", "bio_meso": "Mesomorfo", "bio_endo": "Endomorfo",
            "obj_hiper": "Hipertrofia", "obj_emag": "Emagrecimento", "obj_res": "Resistência",
            "btn_editar": "✏️ Editar", "btn_excluir": "🗑️ Excluir",
            "btn_atualizar_dados": "Atualizar Dados", "titulo_editando": "Editando Usuário",
            "confirmar": "Confirmar", "msg_registro_removido": "Registro removido do banco.",
            "msg_id_nao_localizado": "ID não localizado.", "msg_informe_id_editar": "Informe o ID do usuário para editar.",
            "msg_informe_id_excluir": "Informe o ID para exclusão.", "msg_usuario_nao_encontrado": "Usuário não encontrado.",
            "hdr_id": "ID", "hdr_nome": "Nome", "hdr_biotipo": "Biotipo", "hdr_imc": "IMC"
        },
        "en": {
            "app_titulo": "FitLogic - Integrated Prescription System",
            "btn_alunos": "Students (Ctrl+U)",
            "btn_exercicios": "Exercises (Ctrl+E)",
            "btn_gerar_treinos": "Generate Workouts (Ctrl+T)",

            "btn_nav_alunos": "Students (Ctrl+U)",
            "btn_nav_exercicios": "Exercises (Ctrl+E)",
            "btn_nav_treinos": "Gen Workouts (Ctrl+T)",
            
            "titulo_usuarios": "User Registration",
            "lbl_nome": "Full Name:",
            "lbl_peso": "Weight (kg):",
            "lbl_altura": "Height (m):",
            "lbl_biotipo": "Biotype:",
            "lbl_objetivo": "Objective:",
            "btn_salvar_usuario": "Save User",
            "btn_cancelar_edicao": "Cancel Edition",
            "titulo_lista_usuarios": "Registered Users",

            "titulo_exercicios": "Exercise Registration",
            "lbl_nome_exercicio": "Exercise Name:",
            "lbl_grupo_muscular": "Muscle Group:",
            "lbl_breve_descricao": "Short Description:",
            "lbl_descricao": "Short Description:",
            "btn_salvar_exercicio": "Save Exercise",
            "titulo_catalogo": "Exercise Catalog",
            "titulo_lista_exercicios": "Exercise Catalog",
            "hdr_exercicio": "Exercise",
            "hdr_grupo": "Muscle Group",
            
            "sucesso": "Success",
            "erro": "Error",
            "aviso": "Warning",
            "msg_usuario_cadastrado": "User registered successfully!",
            "msg_usuario_atualizado": "User updated successfully!",
            "msg_exercicio_cadastrado": "Exercise added to catalog!",
            "msg_exercicio_atualizado": "Exercise modified successfully!",
            "msg_confirmar_exclusao": "Are you sure you want to permanently delete ID {}?",

            "lbl_sexo": "Sex:",
            "ph_descricao": "Describe health problems or muscle discomfort...",
            "sexo_m": "Male", "sexo_f": "Female", "sexo_ni": "Prefer not to say",
            "bio_ecto": "Ectomorph", "bio_meso": "Mesomorph", "bio_endo": "Endomorph",
            "obj_hiper": "Hypertrophy", "obj_emag": "Weight Loss", "obj_res": "Endurance",
            "btn_editar": "✏️ Edit", "btn_excluir": "🗑️ Delete",
            "btn_atualizar_dados": "Update Data", "titulo_editando": "Editing User",
            "confirmar": "Confirm", "msg_registro_removido": "Record removed from the database.",
            "msg_id_nao_localizado": "ID not found.", "msg_informe_id_editar": "Enter the user ID to edit.",
            "msg_informe_id_excluir": "Enter the ID to delete.", "msg_usuario_nao_encontrado": "User not found.",
            "hdr_id": "ID", "hdr_nome": "Name", "hdr_biotipo": "Biotype", "hdr_imc": "BMI"
        },
        "es": {
            "app_titulo": "FitLogic - Sistema Integrado de Prescripción",
            "btn_alunos": "Alumnos (Ctrl+U)",
            "btn_exercicios": "Ejercicios (Ctrl+E)",
            "btn_gerar_treinos": "Generar Entrenamientos (Ctrl+T)",

            "btn_nav_alunos": "Alumnos (Ctrl+U)",  # CORRIGIDO: Corrigido de "Alunos" para "Alumnos"
            "btn_nav_exercicios": "Ejercicios (Ctrl+E)",
            "btn_nav_treinos": "Generar Entrenos (Ctrl+T)",
            
            "titulo_usuarios": "Registro de Usuario",
            "lbl_nome": "Nombre Completo:",
            "lbl_peso": "Peso (kg):",
            "lbl_altura": "Altura (m):",
            "lbl_biotipo": "Biotipo:",
            "lbl_objetivo": "Objetivo:",
            "btn_salvar_usuario": "Guardar Usuario",
            "btn_cancelar_edicao": "Cancelar Edición",
            "titulo_lista_usuarios": "Usuarios Registrados",

            "titulo_exercicios": "Registro de Ejercicio",
            "lbl_nome_exercicio": "Nombre del Ejercicio:",
            "lbl_grupo_muscular": "Grupo Muscular:",
            "lbl_breve_descricao": "Breve Descripción:",
            "lbl_descricao": "Descripción Breve:",
            "btn_salvar_exercicio": "Guardar Ejercicio",
            "titulo_catalogo": "Catálogo de Ejercicios",
            "titulo_lista_exercicios": "Catálogo de Ejercicios",
            "hdr_exercicio": "Ejercicio",
            "hdr_grupo": "Grupo Muscular",
            
            "acerto": "Éxito",
            "erro": "Error",
            "aviso": "Aviso",
            "msg_usuario_cadastrado": "¡Usuario registrado con éxito!",
            "msg_usuario_atualizado": "¡Usuario actualizado con éxito!",
            "msg_exercicio_cadastrado": "¡Ejercicio añadido al catálogo!",
            "msg_exercicio_atualizado": "¡Ejercicio modificado con éxito!",
            "msg_confirmar_exclusao": "¿Está seguro de que deseja eliminar el ID {} permanentemente?",

            "lbl_sexo": "Sexo:",
            "ph_descricao": "Describa problemas de salud o molestias musculares...",
            "sexo_m": "Masculino", "sexo_f": "Femenino", "sexo_ni": "Prefiero no informar",
            "bio_ecto": "Ectomorfo", "bio_meso": "Mesomorfo", "bio_endo": "Endomorfo",
            "obj_hiper": "Hipertrofia", "obj_emag": "Adelgazamiento", "obj_res": "Resistencia",
            "btn_editar": "✏️ Editar", "btn_excluir": "🗑️ Eliminar",
            "btn_atualizar_dados": "Actualizar Datos", "titulo_editando": "Editing User",
            "confirmar": "Confirmar", "msg_registro_removido": "Registro eliminado de la base de datos.",
            "msg_id_nao_localizado": "ID no localizado.", "msg_informe_id_editar": "Ingrese el ID del usuario para editar.",
            "msg_informe_id_excluir": "Ingrese el ID para la eliminación.", "msg_usuario_nao_encontrado": "Usuario no encontrado.",
            "hdr_id": "ID", "hdr_nome": "Nombre", "hdr_biotipo": "Biotipo", "hdr_imc": "IMC"
        }
    }

    @classmethod
    def inicializar(cls):
        """Detecta automaticamente o idioma do SO, priorizando o terminal para testes rápidos."""
        # 1. Checa primeiro as variáveis de ambiente (permite forçar pelo terminal do VSCode)
        for env_var in ['LANG', 'LC_ALL', 'LC_MESSAGES']:
            lang_env = os.environ.get(env_var)
            if lang_env:
                # Trata formatos como 'es_ES', 'es' ou 'es_ES.UTF-8'
                sigla = lang_env.split('_')[0].split('.')[0].lower()
                if sigla in cls._traducoes:
                    cls._idioma_ativo = sigla
                    return

        # 2. Se não tiver nada no terminal, pega o padrão nativo do Windows/SO
        try:
            lang, _ = locale.getdefaultlocale()
            if lang:
                sigla = lang.split('_')[0].lower()
                if sigla in cls._traducoes:
                    cls._idioma_ativo = sigla
                    return
        except Exception:
            pass
        
    @classmethod
    def t(cls, chave):
        """Retorna o termo traduzido com base na chave informada."""
        return cls._traducoes[cls._idioma_ativo].get(chave, chave)