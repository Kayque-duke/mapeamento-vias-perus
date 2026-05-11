import urllib.request
import json
import urllib.parse
import time

streets = [
    'Rua Mar do Norte',
    'Rua Mar das Flores',
    'Rua Mar da Irlanda',
    'Rua Ilha de Bali',
    'Rua Guaratinga',
    'Rua Sapucainha',
    'Rua das Alpinas',
    'Rua do Cerrado Brasileiro',
    'Rua do Marajó',
    'Rua Ilhas Britânicas',
    'Rua Albert Jansen',
    'Rua Artur de Azevedo',
    'Alameda Aristoteles Claudio Sbrigh',
    'Rua Ana Maria Franco Laranjeiras',
    'Rua Cleonice Kammer di Sandro',
    'Rua Vieira de Brito',
    'Rua Miguel Vilela',
    'Travessa Cambaratiba',
    'Rua Chamburcy',
    'Travessa Lobito'
]

results = {}
for street in streets:
    query = f'[out:json];way["name"~"{street}",i](around:15000,-23.407,-46.756);out geom;'
    encoded_query = urllib.parse.quote(query)
    req = urllib.request.Request('https://overpass-api.de/api/interpreter?data=' + encoded_query, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data['elements']:
                geom = data['elements'][0].get('geometry', [])
                if geom:
                    avg_lat = sum(g['lat'] for g in geom) / len(geom)
                    avg_lon = sum(g['lon'] for g in geom) / len(geom)
                    results[street] = {'lat': avg_lat, 'lon': avg_lon}
                else:
                    results[street] = 'No geometry'
            else:
                results[street] = 'Not found'
    except Exception as e:
        results[street] = f'Error: {str(e)}'
    time.sleep(1.5)

with open('routes_coords.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print('Done fetching routes')
