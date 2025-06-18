import os
import xlsxwriter

# --- Função Auxiliar ---
# Recebe uma aba e os dados, e cuida de toda a escrita e formatação para não repetir código.
def escrever_dados_na_planilha(workbook, worksheet, dados):
    # Define os formatos de célula que serão usados na planilha.
    formato_cabecalho = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'bg_color': '#D9D9D9'})
    formato_borda = workbook.add_format({'border': 1})
    formato_total = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D9D9D9'})
    vermelho = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    amarelo = workbook.add_format({'bg_color': '#FFEB9C', 'font_color': '#9C5700'})
    verde = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
    
    # Configura o layout inicial da aba: congela o painel e escreve o cabeçalho.
    worksheet.freeze_panes(1, 0)
    worksheet.write_row('A1', ['Defeito', 'Fotos', 'Bicos'], formato_cabecalho)

    # Itera sobre a lista de dados recebida e escreve cada linha na planilha.
    lin = 1
    for chave, fotos, bicos in dados:
        worksheet.write(lin, 0, chave, formato_borda)
        worksheet.write(lin, 1, fotos, formato_borda)
        worksheet.write(lin, 2, bicos, formato_borda)
        lin += 1
    
    # Define as linhas de início e fim para usar nas fórmulas e formatação.
    lin_ini = 2
    lin_fin = lin

    # Aplica o autofiltro e ajusta a largura das colunas.
    worksheet.autofilter(f'A1:C{lin_fin}')
    worksheet.set_column('A:A', 50)
    worksheet.set_column('B:C', 8)

    # Aplica a formatação condicional de cores com base no número de fotos.
    # A verificação evita erros caso a lista de dados esteja vazia.
    range_formatacao = f'B{lin_ini}:C{lin_fin}'
    if lin_ini <= lin_fin:
        worksheet.conditional_format(range_formatacao, {'type': 'formula', 'criteria': f'=$B{lin_ini}<50', 'format': vermelho})
        worksheet.conditional_format(range_formatacao, {'type': 'formula', 'criteria': f'=$B{lin_ini}>=150', 'format': verde})
        worksheet.conditional_format(range_formatacao, {'type': 'formula', 'criteria': f'=AND($B{lin_ini}>=50, $B{lin_ini}<=149)', 'format': amarelo})
    
    # Escreve a linha de 'Total' no final, com as fórmulas de soma.
    worksheet.write(lin, 0, 'Total', formato_total)
    worksheet.write(lin, 1, f'=SUM(B{lin_ini}:B{lin_fin})', formato_total)
    worksheet.write(lin, 2, f'=SUM(C{lin_ini}:C{lin_fin})', formato_total)

# --- Início do Script Principal ---
workbook = xlsxwriter.Workbook('Fotos.xlsx')
comeco_caminho = "Projetos\Contador_de_fotos\Info"

# --- FASE 1: DESCOBERTA DE TIPOS VÁLIDOS ---
# O script varre as pastas de data para descobrir os nomes de tipos válidos.
tipos_conhecidos = set() # Um conjunto para armazenar os tipos encontrados, evitando duplicatas.

for pasta_nome in os.listdir(comeco_caminho):
    # O script considera apenas pastas na raiz que começam com uma data (8 dígitos).
    primeira_parte = pasta_nome.split('_')[0]
    if not (len(primeira_parte) == 8 and primeira_parte.isdigit()):
        continue 
    caminho_pasta = os.path.join(comeco_caminho, pasta_nome)

    # Extrai o tipo de pastas no formato 'Data_com_Tipo'.
    if '_' in pasta_nome:
        tipo_descoberto = '_'.join(pasta_nome.split('_')[1:])
        tipos_conhecidos.add(tipo_descoberto)
    # Para pastas no formato 'Data', os tipos são as subpastas.
    else:
        for tipo_descoberto in os.listdir(caminho_pasta):
            if os.path.isdir(os.path.join(caminho_pasta, tipo_descoberto)):
                tipos_conhecidos.add(tipo_descoberto)

# --- FASE 2: PROCESSAMENTO FILTRADO ---
# O script processa os dados, usando os tipos aprendidos na Fase 1 como filtro.
fotos_por_defeito = {}
for pasta_raiz_nome in os.listdir(comeco_caminho):
    # Filtro: A pasta só é processada se começar com data OU for um tipo já conhecido.
    primeira_parte_raiz = pasta_raiz_nome.split('_')[0]
    if not (len(primeira_parte_raiz) == 8 and primeira_parte_raiz.isdigit()) and pasta_raiz_nome not in tipos_conhecidos:
        continue

    # Verifica a estrutura interna para encontrar o caminho correto das pastas de tipo.
    caminho_raiz = os.path.join(comeco_caminho, pasta_raiz_nome)
    if not os.path.isdir(caminho_raiz): continue
    pastas_tipo_para_processar = []
    subpastas = [p for p in os.listdir(caminho_raiz) if os.path.isdir(os.path.join(caminho_raiz, p))]
    if not subpastas: continue
    caminho_primeira_subpasta = os.path.join(caminho_raiz, subpastas[0])
    if not any(os.path.isdir(os.path.join(caminho_primeira_subpasta, neto)) for neto in os.listdir(caminho_primeira_subpasta)):
        pastas_tipo_para_processar.append({'nome': pasta_raiz_nome, 'caminho': caminho_raiz})
    else:
        for subpasta_nome in subpastas:
            pastas_tipo_para_processar.append({'nome': subpasta_nome, 'caminho': os.path.join(caminho_raiz, subpasta_nome)})
    
    # Para cada pasta de tipo encontrada, o script inicia o processamento dos defeitos.
    for item in pastas_tipo_para_processar:
        tipo_bruto = item['nome']
        caminho_tipo = item['caminho']

        # Remove a data do nome do tipo, se houver.
        partes_tipo = tipo_bruto.split('_')
        if len(partes_tipo) > 1 and len(partes_tipo[0]) == 8 and partes_tipo[0].isdigit():
            tipo = '_'.join(partes_tipo[1:])
        else:
            tipo = tipo_bruto

        for pasta_defeito_nome in os.listdir(caminho_tipo):
            caminho_completo_defeito = os.path.join(caminho_tipo, pasta_defeito_nome)
            if not os.path.isdir(caminho_completo_defeito): continue
            
            # Remove o '_ID' do nome do defeito, se houver.
            if '_ID' in pasta_defeito_nome:
                nome_base_defeito = pasta_defeito_nome[:pasta_defeito_nome.find('_ID')]
            else:
                nome_base_defeito = pasta_defeito_nome

            chave = f"{tipo}/{nome_base_defeito}"
            qnt_fotos = len(os.listdir(caminho_completo_defeito))

            if chave not in fotos_por_defeito:
                fotos_por_defeito[chave] = [0, 0]
            fotos_por_defeito[chave][0] += qnt_fotos
            fotos_por_defeito[chave][1] += 1

# --- PREPARAÇÃO DAS LISTAS DE DADOS PARA AS ABAS ---
dados_todos = []
dados_criticos = []
dados_bons = []

# Primeiro, cria a lista com todos os dados, já ordenada pela chave.
for chave, (fotos, bicos) in sorted(fotos_por_defeito.items()):
    dados_todos.append((chave, fotos, bicos))

# A partir da lista completa, cria as listas filtradas.
for chave, fotos, bicos in dados_todos:
    if fotos >= 150:
        dados_bons.append((chave, fotos, bicos))
    else:
        dados_criticos.append((chave, fotos, bicos))

# --- GERAÇÃO DAS TRÊS ABAS NO EXCEL ---
# Cria as três abas que irão compor o arquivo final.
worksheet_todos = workbook.add_worksheet('Todos os Defeitos')
worksheet_criticos = workbook.add_worksheet('Críticos (Amarelo e Vermelho)')
worksheet_bons = workbook.add_worksheet('Bons (Verde)')

# Chama a função auxiliar para popular cada uma das três abas.
print("Gerando aba 'Todos os Defeitos'...")
escrever_dados_na_planilha(workbook, worksheet_todos, dados_todos)

print("Gerando aba 'Críticos (Amarelo e Vermelho)'...")
escrever_dados_na_planilha(workbook, worksheet_criticos, dados_criticos)

print("Gerando aba 'Bons (Verde)'...")
escrever_dados_na_planilha(workbook, worksheet_bons, dados_bons)

workbook.close()

print("\nPlanilha 'Fotos.xlsx' gerada com sucesso! ✅")