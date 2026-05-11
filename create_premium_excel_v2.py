import xlsxwriter

def create_ultra_premium_excel():
    workbook = xlsxwriter.Workbook('Tabela_MRU_Repeticao_01_Ultra_Premium.xlsx')
    
    # --- GUIAS (Seguindo o princípio de separação de Dados e Dashboard) ---
    ws_dash = workbook.add_worksheet('DASHBOARD')
    ws_data = workbook.add_worksheet('DADOS (Backend)')
    
    # Ocultando as guias de grade (Visual limpo)
    ws_dash.hide_gridlines(2)
    ws_data.hide_gridlines(2)
    
    # =========================================================================
    # BACKEND: GUIA "DADOS (Backend)"
    # =========================================================================
    header_data_fmt = workbook.add_format({
        'bold': True, 'bg_color': '#334155', 'font_color': 'white', 'border': 1, 'border_color': '#475569'
    })
    cell_data_fmt = workbook.add_format({
        'border': 1, 'border_color': '#475569', 'align': 'center'
    })
    cell_data_fmt_num = workbook.add_format({
        'border': 1, 'border_color': '#475569', 'align': 'center', 'num_format': '0.00'
    })
    
    ws_data.set_column('A:C', 20)
    ws_data.write_row('A1', ['Tempo (s)', 'Distância (m)', 'Velocidade Média (m/s)'], header_data_fmt)
    
    data = [
        [0, 0.00],
        [2, 0.35],
        [4, 0.69],
        [6, 1.05],
        [8, 1.38],
        [10, 1.72],
        [12, 2.05]
    ]
    
    for row_num, row_data in enumerate(data):
        row = row_num + 1
        ws_data.write(row, 0, row_data[0], cell_data_fmt)
        ws_data.write(row, 1, row_data[1], cell_data_fmt_num)
        
        # Fórmula exata calculando no backend
        if row_num == 0:
            ws_data.write(row, 2, '---', cell_data_fmt)
        else:
            formula = f'=(B{row+1}-B{row})/(A{row+1}-A{row})'
            ws_data.write_formula(row, 2, formula, cell_data_fmt_num)
            
    # Ocultar a guia de dados para o usuário final ter uma experiência de app?
    # Vamos manter visível mas o foco será 100% no Dashboard.
    
    # =========================================================================
    # FRONTEND: GUIA "DASHBOARD"
    # =========================================================================
    # Paleta de Cores Premium (Dark Theme)
    bg_color = '#0F172A'      # Fundo Principal (Slate 900)
    card_color = '#1E293B'    # Cartões/Células (Slate 800)
    text_main = '#F8FAFC'     # Texto Principal (Slate 50)
    text_muted = '#94A3B8'    # Texto Secundário (Slate 400)
    accent = '#38BDF8'        # Destaque Azul (Sky 400)
    accent_green = '#10B981'  # Destaque Verde (Emerald 500)
    
    # Formatando fundo do Dashboard
    bg_format = workbook.add_format({'bg_color': bg_color})
    for r in range(40):
        ws_dash.set_row(r, 16, bg_format)
    for c in range(25):
        ws_dash.set_column(c, c, 8, bg_format)
        
    # Títulos
    title_fmt = workbook.add_format({
        'bold': True, 'font_size': 22, 'font_color': text_main, 'bg_color': bg_color, 
        'align': 'left', 'valign': 'vcenter'
    })
    subtitle_fmt = workbook.add_format({
        'font_size': 11, 'font_color': accent, 'bg_color': bg_color, 
        'align': 'left', 'valign': 'top'
    })
    
    ws_dash.write('B2', 'ANÁLISE CINEMÁTICA AVANÇADA', title_fmt)
    ws_dash.write('B3', 'MODELAGEM DE SISTEMAS FÍSICOS  |  MRU (REPETIÇÃO 01)  |  POR: KAYQUE RODRIGUES', subtitle_fmt)
    
    # --- CARTÕES KPI (Indicadores Chave de Performance) ---
    kpi_title_fmt = workbook.add_format({
        'bold': True, 'font_size': 9, 'font_color': text_muted, 'bg_color': card_color, 
        'align': 'center', 'valign': 'center', 'top': 1, 'left': 1, 'right': 1, 'border_color': bg_color
    })
    kpi_val_time = workbook.add_format({
        'bold': True, 'font_size': 20, 'font_color': text_main, 'bg_color': card_color, 
        'align': 'center', 'valign': 'center', 'bottom': 1, 'left': 1, 'right': 1, 'border_color': bg_color, 'num_format': '0" s"'
    })
    kpi_val_dist = workbook.add_format({
        'bold': True, 'font_size': 20, 'font_color': accent, 'bg_color': card_color, 
        'align': 'center', 'valign': 'center', 'bottom': 1, 'left': 1, 'right': 1, 'border_color': bg_color, 'num_format': '0.00" m"'
    })
    kpi_val_vel = workbook.add_format({
        'bold': True, 'font_size': 20, 'font_color': accent_green, 'bg_color': card_color, 
        'align': 'center', 'valign': 'center', 'bottom': 1, 'left': 1, 'right': 1, 'border_color': bg_color, 'num_format': '0.000" m/s"'
    })
    
    # Configurar altura das linhas dos KPIs
    ws_dash.set_row(5, 20)
    ws_dash.set_row(6, 40)
    
    # KPI 1: Tempo Total
    ws_dash.merge_range('C5:D5', 'TEMPO TOTAL', kpi_title_fmt)
    ws_dash.merge_range('C6:D6', '=\'DADOS (Backend)\'!A8', kpi_val_time)
    
    # KPI 2: Distância Total
    ws_dash.merge_range('F5:G5', 'DISTÂNCIA TOTAL', kpi_title_fmt)
    ws_dash.merge_range('F6:G6', '=\'DADOS (Backend)\'!B8', kpi_val_dist)
    
    # KPI 3: Velocidade Média (Média das velocidades dos intervalos)
    ws_dash.merge_range('I5:K5', 'VELOCIDADE MÉDIA GLOBAL', kpi_title_fmt)
    ws_dash.merge_range('I6:K6', '=AVERAGE(\'DADOS (Backend)\'!C3:C8)', kpi_val_vel)
    
    # --- TABELA DE APRESENTAÇÃO ---
    # Espaçamento
    ws_dash.set_column('B:B', 3)
    ws_dash.set_column('C:C', 18)
    ws_dash.set_column('D:D', 18)
    ws_dash.set_column('E:E', 22)
    
    tbl_head_fmt = workbook.add_format({
        'bold': True, 'font_color': bg_color, 'bg_color': accent, 
        'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': bg_color
    })
    tbl_cell_fmt = workbook.add_format({
        'font_color': text_main, 'bg_color': card_color, 'align': 'center', 
        'valign': 'vcenter', 'border': 1, 'border_color': bg_color
    })
    tbl_cell_num_fmt = workbook.add_format({
        'font_color': text_main, 'bg_color': card_color, 'align': 'center', 
        'valign': 'vcenter', 'border': 1, 'border_color': bg_color, 'num_format': '0.00'
    })
    
    ws_dash.write('C9', 'Tempo (s)', tbl_head_fmt)
    ws_dash.write('D9', 'Distância (m)', tbl_head_fmt)
    ws_dash.write('E9', 'Vel. Média (m/s)', tbl_head_fmt)
    ws_dash.set_row(8, 25)
    
    for i in range(7):
        row = 9 + i
        ws_dash.set_row(row, 22)
        ws_dash.write_formula(row, 2, f'=\'DADOS (Backend)\'!A{i+2}', tbl_cell_fmt)
        ws_dash.write_formula(row, 3, f'=\'DADOS (Backend)\'!B{i+2}', tbl_cell_num_fmt)
        
        if i == 0:
            ws_dash.write(row, 4, '---', tbl_cell_fmt)
        else:
            ws_dash.write_formula(row, 4, f'=\'DADOS (Backend)\'!C{i+2}', tbl_cell_num_fmt)
            
    # --- GRÁFICO (Dark Mode Integrado) ---
    chart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight_with_markers'})
    chart.add_series({
        'name': 'Modelagem',
        'categories': ['DADOS (Backend)', 1, 0, 7, 0],
        'values':     ['DADOS (Backend)', 1, 1, 7, 1],
        'marker': {'type': 'circle', 'size': 8, 'border': {'color': accent}, 'fill': {'color': card_color}},
        'line': {'color': accent, 'width': 2.5},
        'trendline': {
            'type': 'linear',
            'display_equation': True,
            'display_r_squared': True,
            'line': {'color': accent_green, 'width': 2, 'dash_type': 'dash'},
            'name': 'Tendência Linear'
        }
    })
    
    # Formatando elementos do gráfico para o modo escuro
    chart.set_title({
        'name': 'COMPORTAMENTO CINEMÁTICO (s × m)', 
        'name_font': {'size': 12, 'color': text_main, 'bold': True}
    })
    chart.set_x_axis({
        'name': 'Tempo (s)', 
        'name_font': {'color': text_muted}, 
        'num_font': {'color': text_muted}, 
        'major_gridlines': {'visible': True, 'line': {'color': '#334155', 'dash_type': 'dash'}},
        'line': {'color': '#475569'}
    })
    chart.set_y_axis({
        'name': 'Distância (m)', 
        'name_font': {'color': text_muted}, 
        'num_font': {'color': text_muted}, 
        'major_gridlines': {'visible': True, 'line': {'color': '#334155', 'dash_type': 'dash'}},
        'line': {'color': '#475569'}
    })
    chart.set_legend({'position': 'bottom', 'font': {'color': text_muted}})
    
    # Cor de fundo do gráfico transparente para o dashboard
    chart.set_chartarea({'border': {'none': True}, 'fill': {'color': bg_color}})
    chart.set_plotarea({'border': {'none': True}, 'fill': {'color': bg_color}})
    
    # Texto das equações de tendência
    chart.set_drop_lines({'line': {'color': text_muted}})
    
    # Inserir o gráfico
    ws_dash.insert_chart('G9', chart, {'x_scale': 1.4, 'y_scale': 1.15})
    
    workbook.close()
    print("Arquivo Tabela_MRU_Repeticao_01_Ultra_Premium.xlsx criado com sucesso!")

if __name__ == "__main__":
    create_ultra_premium_excel()
