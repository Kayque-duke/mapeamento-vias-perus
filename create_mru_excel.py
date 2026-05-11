import xlsxwriter

def create_premium_excel():
    workbook = xlsxwriter.Workbook('Tabela_MRU_Repeticao_01.xlsx')
    worksheet = workbook.add_worksheet('Dados Experimentais')

    # --- DEFINIÇÃO DE ESTILOS (Genius Excel Master: "Apresentação Impecável") ---
    title_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'font_color': '#FFFFFF',
        'bg_color': '#111827', # Tema escuro premium
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#374151'
    })

    header_format = workbook.add_format({
        'bold': True,
        'font_size': 11,
        'font_color': '#F9FAFB',
        'bg_color': '#1F2937',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#374151',
        'bottom': 2,
        'bottom_color': '#3B82F6' # Detalhe em azul moderno
    })

    data_format = workbook.add_format({
        'font_size': 11,
        'font_color': '#111827',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#E5E7EB',
        'num_format': '0.00' # O rigor técnico esperado (2 casas decimais)
    })

    data_format_time = workbook.add_format({
        'font_size': 11,
        'font_color': '#111827',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#E5E7EB',
        'num_format': '0'
    })

    text_format = workbook.add_format({
        'font_size': 11,
        'font_color': '#6B7280',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'border_color': '#E5E7EB'
    })

    # "Sem gridlines no dashboard — remover para visual limpo"
    worksheet.hide_gridlines(2)

    # Definir larguras das colunas
    worksheet.set_column('A:A', 3)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 22)
    worksheet.set_column('E:I', 15)

    # --- INSERÇÃO DO TÍTULO ---
    worksheet.merge_range('B2:D2', 'ANÁLISE DE MRU: REPETIÇÃO 01', title_format)
    worksheet.set_row(1, 30)

    # --- INSERÇÃO DOS CABEÇALHOS ---
    headers = ['Tempo (s)', 'Distância (m)', 'Velocidade Média (m/s)']
    worksheet.write_row('B4', headers, header_format)
    worksheet.set_row(3, 20)

    # --- INSERÇÃO DOS DADOS ---
    data = [
        [0, 0.00],
        [2, 0.35],
        [4, 0.69],
        [6, 1.05],
        [8, 1.38],
        [10, 1.72],
        [12, 2.05]
    ]

    # Escrever dados e fórmulas automatizadas
    for row_num, row_data in enumerate(data):
        row_excel = 5 + row_num # Começa na linha 5 do Excel
        worksheet.write(row_excel - 1, 1, row_data[0], data_format_time)
        worksheet.write(row_excel - 1, 2, row_data[1], data_format)
        
        # Célula inicial (tempo 0) não tem cálculo de velocidade anterior
        if row_num == 0:
            worksheet.write(row_excel - 1, 3, '---', text_format)
        else:
            # Fórmula: =(C5-C4)/(B5-B4) - O Excel automaticamente adapta ao arrastar, aqui geramos a fórmula exata por linha.
            # O Genius Excel usa cálculos exatos e performáticos.
            formula = f'=(C{row_excel}-C{row_excel-1})/(B{row_excel}-B{row_excel-1})'
            worksheet.write_formula(row_excel - 1, 3, formula, data_format)

    # --- CRIAÇÃO DO GRÁFICO (Dica de Apresentação) ---
    chart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight_with_markers'})

    chart.add_series({
        'name': 'Distância vs Tempo',
        'categories': ['Dados Experimentais', 4, 1, 10, 1], # Tempo
        'values':     ['Dados Experimentais', 4, 2, 10, 2], # Distância
        'marker': {'type': 'circle', 'size': 6, 'border': {'color': '#3B82F6'}, 'fill': {'color': '#FFFFFF'}},
        'line': {'color': '#3B82F6', 'width': 2.25},
        'trendline': {
            'type': 'linear',
            'display_equation': True,
            'display_r_squared': True,
            'line': {'color': '#EF4444', 'width': 1.5, 'dash_type': 'dash'},
            'name': 'Tendência Linear (MRU)'
        }
    })

    chart.set_title({'name': 'Dispersão e Tendência Linear', 'name_font': {'size': 12, 'color': '#111827'}})
    chart.set_x_axis({'name': 'Tempo (s)', 'major_gridlines': {'visible': True, 'line': {'color': '#F3F4F6'}}})
    chart.set_y_axis({'name': 'Distância (m)', 'major_gridlines': {'visible': True, 'line': {'color': '#F3F4F6'}}})
    chart.set_legend({'position': 'bottom'})
    chart.set_chartarea({'border': {'none': True}})

    worksheet.insert_chart('F4', chart, {'x_offset': 10, 'y_offset': 0})

    # --- ANÁLISE QUALITATIVA ---
    analysis_title_format = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'font_color': '#111827',
        'align': 'left',
        'valign': 'vcenter'
    })

    analysis_text_format = workbook.add_format({
        'font_size': 11,
        'font_color': '#4B5563',
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1,
        'border_color': '#E5E7EB',
        'bg_color': '#F9FAFB'
    })

    worksheet.write('B13', 'ANÁLISE QUALITATIVA (CONFIRMAÇÃO MATEMÁTICA):', analysis_title_format)
    texto_analise = (
        "Note que os valores na coluna de Velocidade Média (m/s) ficaram oscilando levemente entre 0,17 e 0,18. "
        "Na prática experimental, essa pequena variação é perfeitamente normal e aceitável, sendo causada por fatores que descrevemos "
        "anteriormente, como o tempo de resposta na marcação ou micro-irregularidades no porcelanato.\n\n"
        "Como os valores são quase idênticos, você tem a confirmação matemática de que o sistema se comporta como um Movimento "
        "Retilíneo Uniforme (MRU). Se a velocidade estivesse aumentando significativamente (ex: 0,10; 0,25; 0,40...), estaríamos "
        "diante de um movimento acelerado, o que invalidaria a nossa modelagem por função linear."
    )
    worksheet.merge_range('B14:D20', texto_analise, analysis_text_format)

    # --- AUTORIA / MARCAÇÃO ---
    author_format = workbook.add_format({
        'font_size': 9,
        'font_color': '#9CA3AF',
        'italic': True,
        'align': 'right'
    })
    worksheet.write('D22', 'Gerado pelo The Genius Excel Master', author_format)

    workbook.close()
    print("Arquivo Excel Tabela_MRU_Repeticao_01.xlsx criado com sucesso!")

if __name__ == "__main__":
    create_premium_excel()
