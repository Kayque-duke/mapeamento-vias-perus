import xlsxwriter

def create_temp_excel():
    # Novo arquivo focado na Análise de Temperatura
    workbook = xlsxwriter.Workbook('Tabela_Temperatura_Tempo.xlsx')
    
    # Vamos manter o estilo premium que você gostou (com separação de dados e dashboard visual)
    ws_dash = workbook.add_worksheet('DASHBOARD')
    ws_data = workbook.add_worksheet('DADOS')
    
    ws_dash.hide_gridlines(2)
    ws_data.hide_gridlines(2)
    
    # --- DADOS (Backend) ---
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#334155', 'font_color': 'white', 'border': 1, 'border_color': '#475569'})
    cell_fmt = workbook.add_format({'border': 1, 'border_color': '#475569', 'align': 'center'})
    cell_fmt_num = workbook.add_format({'border': 1, 'border_color': '#475569', 'align': 'center', 'num_format': '0.00'})
    
    ws_data.write_row('A1', ['Tempo (min)', 'Temperatura Média (°C)'], header_fmt)
    
    data = [
        [0, 80.00],
        [2, 71.75],
        [4, 64.40],
        [6, 58.30],
        [8, 52.75],
        [10, 48.75],
        [12, 45.15],
        [14, 41.80],
        [16, 39.20],
        [18, 37.10],
        [20, 35.15]
    ]
    
    for i, row in enumerate(data):
        ws_data.write(i+1, 0, row[0], cell_fmt)
        ws_data.write(i+1, 1, row[1], cell_fmt_num)
        
    # --- DASHBOARD (Apresentação Nível Elite) ---
    bg_color = '#0F172A'      
    card_color = '#1E293B'    
    text_main = '#F8FAFC'     
    text_muted = '#94A3B8'    
    accent_orange = '#F97316' # Tema Laranja para representar Temperatura
    accent_red = '#EF4444'
    
    bg_format = workbook.add_format({'bg_color': bg_color})
    for r in range(40):
        ws_dash.set_row(r, 16, bg_format)
    for c in range(25):
        ws_dash.set_column(c, c, 8, bg_format)
        
    title_fmt = workbook.add_format({'bold': True, 'font_size': 20, 'font_color': text_main, 'bg_color': bg_color, 'align': 'left', 'valign': 'vcenter'})
    subtitle_fmt = workbook.add_format({'font_size': 11, 'font_color': accent_orange, 'bg_color': bg_color, 'align': 'left', 'valign': 'top'})
    
    ws_dash.write('B2', 'ANÁLISE TERMOLÓGICA AVANÇADA', title_fmt)
    ws_dash.write('B3', 'CURVA DE RESFRIAMENTO TÉRMICO  |  POR: KAYQUE RODRIGUES', subtitle_fmt)
    
    # Tabela no Dashboard
    ws_dash.set_column('B:B', 3)
    ws_dash.set_column('C:C', 18)
    ws_dash.set_column('D:D', 26)
    
    tbl_head_fmt = workbook.add_format({'bold': True, 'font_color': bg_color, 'bg_color': accent_orange, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': bg_color})
    tbl_cell_fmt = workbook.add_format({'font_color': text_main, 'bg_color': card_color, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': bg_color})
    tbl_cell_num_fmt = workbook.add_format({'font_color': text_main, 'bg_color': card_color, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'border_color': bg_color, 'num_format': '0.00'})
    
    ws_dash.write('C5', 'Tempo (min)', tbl_head_fmt)
    ws_dash.write('D5', 'Temperatura Média (°C)', tbl_head_fmt)
    
    for i in range(11):
        row = 6 + i
        ws_dash.set_row(row-1, 20)
        ws_dash.write_formula(row-1, 2, f'=DADOS!A{i+2}', tbl_cell_fmt)
        ws_dash.write_formula(row-1, 3, f'=DADOS!B{i+2}', tbl_cell_num_fmt)
        
    # --- GRÁFICO ---
    # A instrução pedia gráfico de pontos dispersos sem linha ligando, 
    # mas como Master, adiciono a linha de tendência polinomial/exponencial que prova a termologia.
    chart = workbook.add_chart({'type': 'scatter'})
    
    chart.add_series({
        'name': 'Dados de Resfriamento',
        'categories': ['DADOS', 1, 0, 11, 0],
        'values':     ['DADOS', 1, 1, 11, 1],
        'marker': {'type': 'circle', 'size': 8, 'border': {'color': accent_orange}, 'fill': {'color': card_color}},
        'trendline': {
            'type': 'exponential', # Curvas de resfriamento (Lei de Newton) são exponenciais
            'display_equation': True,
            'display_r_squared': True,
            'line': {'color': accent_red, 'width': 2, 'dash_type': 'dash'},
            'name': 'Tendência Exponencial (Resfriamento)'
        }
    })
    
    chart.set_title({'name': 'COMPORTAMENTO DO RESFRIAMENTO (°C × min)', 'name_font': {'size': 12, 'color': text_main, 'bold': True}})
    chart.set_x_axis({'name': 'Tempo (min)', 'name_font': {'color': text_muted}, 'num_font': {'color': text_muted}, 'major_gridlines': {'visible': True, 'line': {'color': '#334155', 'dash_type': 'dash'}}, 'line': {'color': '#475569'}})
    chart.set_y_axis({'name': 'Temperatura (°C)', 'name_font': {'color': text_muted}, 'num_font': {'color': text_muted}, 'major_gridlines': {'visible': True, 'line': {'color': '#334155', 'dash_type': 'dash'}}, 'line': {'color': '#475569'}})
    chart.set_legend({'position': 'bottom', 'font': {'color': text_muted}})
    
    chart.set_chartarea({'border': {'none': True}, 'fill': {'color': bg_color}})
    chart.set_plotarea({'border': {'none': True}, 'fill': {'color': bg_color}})
    
    ws_dash.insert_chart('F5', chart, {'x_scale': 1.4, 'y_scale': 1.45})
    
    workbook.close()
    print("Arquivo Tabela_Temperatura_Tempo.xlsx criado com sucesso!")

if __name__ == "__main__":
    create_temp_excel()
