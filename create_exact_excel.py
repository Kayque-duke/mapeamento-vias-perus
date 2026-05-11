import xlsxwriter

def create_exact_excel():
    workbook = xlsxwriter.Workbook('Tabela_MRU_Exata_Professor.xlsx')
    
    # Criando as Abas exigidas
    ws1 = workbook.add_worksheet('Dados Brutos')
    ws2 = workbook.add_worksheet('Análise MRU')
    
    # Ocultar linhas de grade para visual Premium
    ws1.hide_gridlines(2)
    ws2.hide_gridlines(2)
    
    # Formatação Profissional
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#1E293B', 'font_color': 'white', 'border': 1, 'border_color': '#CBD5E1', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
    cell_fmt = workbook.add_format({'border': 1, 'border_color': '#CBD5E1', 'align': 'center', 'valign': 'vcenter'})
    cell_num_2 = workbook.add_format({'border': 1, 'border_color': '#CBD5E1', 'align': 'center', 'valign': 'vcenter', 'num_format': '0.00'})
    cell_num_3 = workbook.add_format({'border': 1, 'border_color': '#CBD5E1', 'align': 'center', 'valign': 'vcenter', 'num_format': '0.000'})
    title_fmt = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#0F172A'})
    
    # =========================================================================
    # PASSO 1: ABA 1 (Dados Brutos)
    # =========================================================================
    ws1.set_column('A:A', 12)
    ws1.set_column('B:D', 18)
    ws1.set_column('E:F', 24)
    ws1.set_row(0, 30)
    
    headers1 = ['Tempo (s)', 'Repetição 1 (m)', 'Repetição 2 (m)', 'Repetição 3 (m)', 'Média Consolidada (m)', 'Desvio-Padrão (m)']
    ws1.write_row('A1', headers1, header_fmt)
    
    data1 = [
        [0, 0.00, 0.00, 0.00],
        [2, 0.35, 0.36, 0.34],
        [4, 0.69, 0.70, 0.68],
        [6, 1.05, 1.03, 1.07],
        [8, 1.38, 1.37, 1.39],
        [10, 1.72, 1.74, 1.70],
        [12, 2.05, 2.06, 2.04]
    ]
    
    for i, row in enumerate(data1):
        r = i + 1  # Linhas do Excel (0-indexed no xlsxwriter, então 1 é Linha 2)
        ws1.set_row(r, 20)
        ws1.write(r, 0, row[0], cell_fmt)
        ws1.write(r, 1, row[1], cell_num_2)
        ws1.write(r, 2, row[2], cell_num_2)
        ws1.write(r, 3, row[3], cell_num_2)
        
        # Fórmulas de Média e Desvio (em inglês nativo do Excel: AVERAGE e STDEV.S)
        ws1.write_formula(r, 4, f'=AVERAGE(B{r+1}:D{r+1})', cell_num_2)
        if i == 0:
            ws1.write(r, 5, 0.000, cell_num_3)
        else:
            ws1.write_formula(r, 5, f'=STDEV.S(B{r+1}:D{r+1})', cell_num_3)
            
    # =========================================================================
    # PASSO 2: ABA 2 (Análise MRU)
    # =========================================================================
    ws2.set_column('A:B', 24)
    ws2.set_column('C:C', 26)
    ws2.set_row(2, 30)
    
    # 1. Título em A1
    ws2.write('A1', 'ANÁLISE DE MRU: MÉDIA CONSOLIDADA (3 REPETIÇÕES)', title_fmt)
    
    # 2. Cabeçalhos na Linha 3 (A3:C3 no Excel -> row=2 no xlsxwriter)
    headers2 = ['Tempo (s)', 'Distância Consolidada (m)', 'Velocidade Média (m/s)']
    ws2.write_row('A3', headers2, header_fmt)
    
    # 3. Dados
    data2 = [
        [0, 0.00, None],
        [2, 0.35, 0.18],
        [4, 0.69, 0.17],
        [6, 1.05, 0.18],
        [8, 1.38, 0.17],
        [10, 1.72, 0.17],
        [12, 2.05, 0.17]
    ]
    
    for i, row in enumerate(data2):
        r = i + 3 # Linha 4 no Excel
        ws2.set_row(r, 20)
        ws2.write(r, 0, row[0], cell_fmt)
        ws2.write(r, 1, row[1], cell_num_2)
        
        if row[2] is None:
            ws2.write(r, 2, '-', cell_fmt)
        else:
            ws2.write(r, 2, row[2], cell_num_2)
            
    # 4. Gráfico de Dispersão
    chart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight_with_markers'})
    
    chart.add_series({
        'name': 'Cinemática MRU',
        'categories': ['Análise MRU', 3, 0, 9, 0], # A4:A10
        'values':     ['Análise MRU', 3, 1, 9, 1], # B4:B10
        'marker': {'type': 'circle', 'size': 7, 'border': {'color': '#0369A1'}, 'fill': {'color': '#FFFFFF'}},
        'line': {'color': '#0369A1', 'width': 2},
        'trendline': {
            'type': 'linear',
            'display_equation': True,
            'display_r_squared': True,
            'line': {'color': '#B91C1C', 'width': 1.5, 'dash_type': 'dash'},
        }
    })
    
    chart.set_title({'name': 'Posição × Tempo', 'name_font': {'size': 12, 'bold': True}})
    chart.set_x_axis({'name': 'Tempo (s)', 'major_gridlines': {'visible': True, 'line': {'color': '#E2E8F0', 'dash_type': 'dash'}}})
    chart.set_y_axis({'name': 'Distância (m)', 'major_gridlines': {'visible': True, 'line': {'color': '#E2E8F0', 'dash_type': 'dash'}}})
    chart.set_legend({'none': True})
    chart.set_chartarea({'border': {'color': '#CBD5E1'}})
    
    ws2.insert_chart('E3', chart, {'x_scale': 1.3, 'y_scale': 1.3})
    
    workbook.close()
    print("Arquivo Tabela_MRU_Exata_Professor.xlsx criado com sucesso!")

if __name__ == "__main__":
    create_exact_excel()
