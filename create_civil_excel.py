import xlsxwriter

def create_civil_excel():
    workbook = xlsxwriter.Workbook('Tabela_Analise_Repeticoes_MRU.xlsx')
    
    # Arquitetura de Planilha Nível Engenharia Sênior
    ws_dash = workbook.add_worksheet('RELATÓRIO TÉCNICO')
    ws_data = workbook.add_worksheet('DADOS (Backend)')
    
    ws_dash.hide_gridlines(2)
    ws_data.hide_gridlines(2)
    
    # =========================================================================
    # BACKEND: GUIA "DADOS"
    # =========================================================================
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#334155', 'font_color': 'white', 'border': 1, 'border_color': '#475569'})
    cell_fmt = workbook.add_format({'border': 1, 'border_color': '#475569', 'align': 'center'})
    cell_fmt_num_2 = workbook.add_format({'border': 1, 'border_color': '#475569', 'align': 'center', 'num_format': '0.00'})
    cell_fmt_num_3 = workbook.add_format({'border': 1, 'border_color': '#475569', 'align': 'center', 'num_format': '0.000'})
    
    headers = ['Tempo (s)', 'Distância Rep. 1 (m)', 'Distância Rep. 2 (m)', 'Distância Rep. 3 (m)', 'Média Consolidada (m)', 'Desvio-Padrão (m)']
    ws_data.write_row('A1', headers, header_fmt)
    
    data = [
        [0, 0.00, 0.00, 0.00],
        [2, 0.35, 0.36, 0.34],
        [4, 0.69, 0.70, 0.68],
        [6, 1.05, 1.03, 1.07],
        [8, 1.38, 1.37, 1.39],
        [10, 1.72, 1.74, 1.70],
        [12, 2.05, 2.06, 2.04]
    ]
    
    for i, row in enumerate(data):
        excel_row = i + 1
        ws_data.write(excel_row, 0, row[0], cell_fmt)
        ws_data.write(excel_row, 1, row[1], cell_fmt_num_2)
        ws_data.write(excel_row, 2, row[2], cell_fmt_num_2)
        ws_data.write(excel_row, 3, row[3], cell_fmt_num_2)
        
        # Fórmulas Automatizadas do Excel para Média e Desvio Padrão
        ws_data.write_formula(excel_row, 4, f'=AVERAGE(B{excel_row+1}:D{excel_row+1})', cell_fmt_num_2)
        
        if i == 0:
            ws_data.write(excel_row, 5, 0.000, cell_fmt_num_3)
        else:
            ws_data.write_formula(excel_row, 5, f'=STDEV.S(B{excel_row+1}:D{excel_row+1})', cell_fmt_num_3)
            
    # =========================================================================
    # FRONTEND: GUIA "RELATÓRIO TÉCNICO" (Estilo Blueprint/Engenharia)
    # =========================================================================
    bg_color = '#F8FAFC'      # Fundo Claro e Limpo (Papel de Relatório Técnico)
    card_color = '#FFFFFF'    # Branco
    text_main = '#0F172A'     # Preto/Azul Muito Escuro
    text_muted = '#475569'    
    accent_blue = '#0F766E'   # Teal Escuro - Tom muito usado em engenharia civil/arquitetura
    
    bg_format = workbook.add_format({'bg_color': bg_color})
    for r in range(45):
        ws_dash.set_row(r, 16, bg_format)
    for c in range(20):
        ws_dash.set_column(c, c, 8, bg_format)
        
    title_fmt = workbook.add_format({'bold': True, 'font_size': 20, 'font_color': text_main, 'bg_color': bg_color, 'align': 'left', 'valign': 'vcenter'})
    subtitle_fmt = workbook.add_format({'font_size': 11, 'font_color': accent_blue, 'bg_color': bg_color, 'align': 'left', 'valign': 'top', 'bold': True})
    
    ws_dash.write('B2', 'ANÁLISE DE MRU: MÉDIA CONSOLIDADA (3 REPETIÇÕES)', title_fmt)
    ws_dash.write('B3', 'CONTROLE DE QUALIDADE E DESVIO PADRÃO  |  ENG. RESP: KAYQUE RODRIGUES', subtitle_fmt)
    
    # Configuração de Larguras da Tabela
    ws_dash.set_column('B:B', 3)
    ws_dash.set_column('C:C', 12)
    ws_dash.set_column('D:F', 20)
    ws_dash.set_column('G:H', 22)
    
    tbl_head_fmt = workbook.add_format({'bold': True, 'font_color': '#FFFFFF', 'bg_color': accent_blue, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': '#CBD5E1', 'text_wrap': True})
    tbl_cell_fmt = workbook.add_format({'font_color': text_main, 'bg_color': card_color, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': '#CBD5E1'})
    tbl_cell_num_2 = workbook.add_format({'font_color': text_main, 'bg_color': card_color, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': '#CBD5E1', 'num_format': '0.00'})
    tbl_cell_num_3 = workbook.add_format({'font_color': text_main, 'bg_color': card_color, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': '#CBD5E1', 'num_format': '0.000'})
    tbl_cell_alert = workbook.add_format({'font_color': '#991B1B', 'bg_color': '#FEE2E2', 'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': '#CBD5E1', 'num_format': '0.000', 'bold': True})
    
    for i, h in enumerate(headers):
        ws_dash.write(4, 2+i, h, tbl_head_fmt)
    
    ws_dash.set_row(4, 35) # Aumentar altura do cabeçalho
    
    # Puxando dados do Backend
    for i in range(7):
        row = 5 + i
        ws_dash.set_row(row, 20)
        ws_dash.write_formula(row, 2, f'=\'DADOS (Backend)\'!A{i+2}', tbl_cell_fmt)
        ws_dash.write_formula(row, 3, f'=\'DADOS (Backend)\'!B{i+2}', tbl_cell_num_2)
        ws_dash.write_formula(row, 4, f'=\'DADOS (Backend)\'!C{i+2}', tbl_cell_num_2)
        ws_dash.write_formula(row, 5, f'=\'DADOS (Backend)\'!D{i+2}', tbl_cell_num_2)
        ws_dash.write_formula(row, 6, f'=\'DADOS (Backend)\'!E{i+2}', tbl_cell_num_2)
        
        # Desvio Padrão
        ws_dash.write_formula(row, 7, f'=\'DADOS (Backend)\'!F{i+2}', tbl_cell_num_3)
        
    # Formatação Condicional Nível Engenharia: Destacar desvios acima do aceitável (ex: >= 0.020)
    ws_dash.conditional_format(5, 7, 11, 7, {
        'type': 'cell',
        'criteria': '>=',
        'value': 0.019,
        'format': tbl_cell_alert
    })
    
    # --- GRÁFICO AVANÇADO (Com Barras de Erro baseadas no Desvio Padrão) ---
    chart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight_with_markers'})
    
    chart.add_series({
        'name': 'Média Consolidada',
        'categories': ['DADOS (Backend)', 1, 0, 7, 0],
        'values':     ['DADOS (Backend)', 1, 4, 7, 4],
        'marker': {'type': 'square', 'size': 7, 'border': {'color': accent_blue}, 'fill': {'color': card_color}},
        'line': {'color': accent_blue, 'width': 2.25},
        # Barras de Erro (Desvio Padrão) - Isso impressiona MUITO na engenharia
        'y_error_bars': {
            'type': 'custom',
            'plus_values':  ['DADOS (Backend)', 1, 5, 7, 5],
            'minus_values': ['DADOS (Backend)', 1, 5, 7, 5],
            'line': {'color': '#991B1B', 'width': 1.2}
        },
        'trendline': {
            'type': 'linear',
            'display_equation': True,
            'display_r_squared': True,
            'line': {'color': text_muted, 'width': 1.5, 'dash_type': 'dash'},
            'name': 'Regressão Linear da Média'
        }
    })
    
    chart.set_title({'name': 'ENSAIO CINEMÁTICO: MÉDIA CONSOLIDADA COM BARRAS DE DESVIO (ERRO)', 'name_font': {'size': 11, 'color': text_main, 'bold': True}})
    chart.set_x_axis({'name': 'Tempo (s)', 'name_font': {'color': text_muted}, 'num_font': {'color': text_muted}, 'major_gridlines': {'visible': True, 'line': {'color': '#E2E8F0', 'dash_type': 'dash'}}})
    chart.set_y_axis({'name': 'Distância (m)', 'name_font': {'color': text_muted}, 'num_font': {'color': text_muted}, 'major_gridlines': {'visible': True, 'line': {'color': '#E2E8F0', 'dash_type': 'dash'}}})
    chart.set_legend({'position': 'bottom'})
    chart.set_chartarea({'border': {'color': '#CBD5E1'}, 'fill': {'color': card_color}})
    chart.set_plotarea({'border': {'color': '#CBD5E1'}, 'fill': {'color': card_color}})
    
    ws_dash.insert_chart('C14', chart, {'x_scale': 1.76, 'y_scale': 1.6})
    
    workbook.close()
    print("Arquivo Tabela_Analise_Repeticoes_MRU.xlsx criado com sucesso!")

if __name__ == "__main__":
    create_civil_excel()
