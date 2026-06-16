import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from app.models.plano_treino import PlanoTreino

class GeradorPDFService:
    @staticmethod
    def exportar_treino(plano: PlanoTreino, filepath: str):
        """Gera um relatório profissional em PDF contendo a ficha de treino customizada."""
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Título Principal
        title_style = ParagraphStyle(
            'TitleStyle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1A237E'), spaceAfter=15
        )
        story.append(Paragraph("FitLogic - Ficha de Treino Personalizada", title_style))
        story.append(Spacer(1, 10))

        # Informações do Aluno
        info_text = (
            f"<b>Aluno:</b> {plano.usuario.nome} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"<b>Biotipo:</b> {plano.usuario.biotipo} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"<b>Objetivo:</b> {plano.usuario.objetivo}<br/>"
            f"<b>Divisão Estrutural:</b> Semanal {plano.divisao_treino} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"<b>Data de Emissão:</b> {plano.data_criacao.strftime('%d/%m/%Y')}"
        )
        story.append(Paragraph(info_text, styles['Normal']))
        story.append(Spacer(1, 20))

        # Tabela de Exercícios
        dados_tabela = [["Exercício", "Grupo Muscular", "Séries", "Repetições", "Descanso"]]
        for item in plano.itens:
            dados_tabela.append([
                item.exercicio.nome,
                item.exercicio.grupo_muscular,
                str(item.series),
                str(item.repeticoes),
                f"{item.descanso_segundos}s"
            ])

        tabela = Table(dados_tabela, colWidths=[180, 110, 60, 80, 70])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A237E')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F5F5F5')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E0E0E0')),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
        ]))
        
        story.append(tabela)
        doc.build(story)