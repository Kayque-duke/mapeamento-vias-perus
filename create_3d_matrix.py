import xlsxwriter

def create_3d_matrix():
    # Criando o arquivo para o Modelo Topográfico
    workbook = xlsxwriter.Workbook('Tabela_Matriz_Topografica_3D.xlsx')
    ws = workbook.add_worksheet('Modelo Topográfico')
    
    # Ocultar linhas de grade para ficar profissional
    ws.hide_gridlines(2)
    
    # Formatação nível Engenharia
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#1E293B', 'font_color': 'white', 'border': 1, 'border_color': '#CBD5E1', 'align': 'center', 'valign': 'vcenter'})
    y_fmt = workbook.add_format({'bold': True, 'bg_color': '#334155', 'font_color': 'white', 'border': 1, 'border_color': '#CBD5E1', 'align': 'center', 'valign': 'vcenter'})
    cell_fmt = workbook.add_format({'border': 1, 'border_color': '#CBD5E1', 'align': 'center', 'valign': 'vcenter', 'num_format': '0.00'})
    
    ws.set_column('A:D', 12)
    ws.set_row(0, 25)
    
    # 1. Montando a Matriz (Eixo X na Horizontal, Eixo Y na Vertical)
    ws.write('A1', 'Y / X', header_fmt)
    ws.write_row('B1', [0, 10, 20], header_fmt)
    
    data = [
        [0, 5.04, 10.01, 14.98],
        [10, 7.04, 12.01, 16.98],
        [20, 9.04, 14.01, 18.98]
    ]
    
    for i, row in enumerate(data):
        r = i + 1
        ws.set_row(r, 20)
        # Eixo Y
        ws.write(r, 0, row[0], y_fmt)
        # Valores de Z (Elevação)
        ws.write_row(r, 1, row[1:], cell_fmt)
        
    # NOTA TÉCNICA: O pacote XlsxWriter não possui suporte nativo à renderização da "Superfície 3D" 
    # (trata-se de um recurso exclusivo do motor gráfico do Excel UI). 
    # Por isso, vamos plotar um Gráfico de Radar (que é a base matemática da superfície) 
    # para servir de "Preview", e o usuário poderá convertê-lo em 2 cliques conforme o tutorial dele.
    
    chart = workbook.add_chart({'type': 'radar', 'subtype': 'filled'})
    
    # Adicionando as séries (as "fatias" da topografia)
    chart.add_series({
        'name': 'Y=0', 
        'categories': ['Modelo Topográfico', 0, 1, 0, 3], 
        'values': ['Modelo Topográfico', 1, 1, 1, 3],
        'fill': {'color': '#0284C7', 'transparency': 40}
    })
    chart.add_series({
        'name': 'Y=10', 
        'categories': ['Modelo Topográfico', 0, 1, 0, 3], 
        'values': ['Modelo Topográfico', 2, 1, 2, 3],
        'fill': {'color': '#0D9488', 'transparency': 40}
    })
    chart.add_series({
        'name': 'Y=20', 
        'categories': ['Modelo Topográfico', 0, 1, 0, 3], 
        'values': ['Modelo Topográfico', 3, 1, 3, 3],
        'fill': {'color': '#F59E0B', 'transparency': 40}
    })
    
    chart.set_title({'name': 'Superfície Tridimensional Interpolada (Modelo Topográfico)', 'name_font': {'size': 12}})
    chart.set_legend({'position': 'bottom'})
    chart.set_chartarea({'border': {'color': '#CBD5E1'}})
    
    # Inserir o gráfico na planilha
    ws.insert_chart('A7', chart, {'x_scale': 1.5, 'y_scale': 1.5})
    
    workbook.close()
    print("Arquivo Tabela_Matriz_Topografica_3D.xlsx criado com sucesso!")

if __name__ == "__main__":
    create_3d_matrix()
