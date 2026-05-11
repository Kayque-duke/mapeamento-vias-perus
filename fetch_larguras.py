import urllib.request
import urllib.parse
import json
import time
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Ruas que precisam de largura real (atualmente com placeholders)
streets_to_check = [
    {"id": 15, "nome": "Rua Francisco Bellazzi", "largura_atual": 6.0},
    {"id": 16, "nome": "Avenida Felippo Sturba", "largura_atual": 7.0},
    {"id": 17, "nome": "Rua Onze", "largura_atual": 4.0},
    {"id": 18, "nome": "Estrada de Pirapora", "largura_atual": 8.0},
    {"id": 19, "nome": "Rua Educador", "largura_atual": 6.0},
    {"id": 20, "nome": "Rua Noel Rosa", "largura_atual": 6.0},
    {"id": 21, "nome": "Rua Carlos Lamarca", "largura_atual": 6.0},
    {"id": 22, "nome": "Rua Ilha da Vitória", "largura_atual": 6.0},
    {"id": 23, "nome": "Rua Nova Vida", "largura_atual": 6.0},
    {"id": 24, "nome": "Rua Nova Canaã", "largura_atual": 6.0},
    {"id": 25, "nome": "Rua Mil Grau", "largura_atual": 6.0},
    {"id": 26, "nome": "Rua Morais", "largura_atual": 6.0},
    {"id": 27, "nome": "Rua Esperança", "largura_atual": 6.0},
    {"id": 28, "nome": "Travessa Cambaratiba", "largura_atual": 5.0},
    {"id": 29, "nome": "Rua Albert Jansen", "largura_atual": 7.0},
    {"id": 30, "nome": "Rua Ilhas Britânicas", "largura_atual": 6.0},
]

# Estimativa de largura por classificação viária
WIDTH_BY_HIGHWAY = {
    'motorway': 12.0,
    'trunk': 11.0,
    'primary': 10.0,
    'secondary': 9.0,
    'tertiary': 8.0,
    'residential': 7.0,
    'unclassified': 6.0,
    'service': 4.0,
    'living_street': 5.0,
    'track': 3.5,
    'footway': 2.0,
    'path': 1.5,
    'pedestrian': 4.0,
    'cycleway': 2.5,
}

def estimate_width(tags):
    """Estima largura baseado nas tags do OSM"""
    if not tags:
        return None, 'Sem dados'
    # 1. Tag 'width' explícita (melhor caso)
    if 'width' in tags:
        try:
            w = tags['width'].replace('m', '').replace(' ', '').replace(',', '.')
            return float(w), 'OSM width tag'
        except:
            pass
    
    # 2. Tag 'est_width' (largura estimada)
    if 'est_width' in tags:
        try:
            w = tags['est_width'].replace('m', '').replace(' ', '').replace(',', '.')
            return float(w), 'OSM est_width tag'
        except:
            pass
    
    # 3. Calcular por número de faixas
    if 'lanes' in tags:
        try:
            lanes = int(tags['lanes'])
            width = lanes * 3.5  # 3.5m por faixa
            return width, f'Calculado ({lanes} faixas x 3.5m)'
        except:
            pass
    
    # 4. Estimar pela classificação viária
    highway = tags.get('highway', '')
    if highway in WIDTH_BY_HIGHWAY:
        return WIDTH_BY_HIGHWAY[highway], f'Estimado (tipo: {highway})'
    
    return None, 'Sem dados'

def query_overpass(street_name):
    """Busca uma rua no Overpass API próxima a Perus"""
    # Tentar múltiplos endpoints
    endpoints = [
        'https://overpass.kumi.systems/api/interpreter',
        'https://overpass-api.de/api/interpreter',
    ]
    
    query = f'[out:json][timeout:10];way["name"~"{street_name}",i]["highway"](around:15000,-23.407,-46.756);out tags;'
    encoded = urllib.parse.urlencode({'data': query}).encode('utf-8')
    
    for ep in endpoints:
        try:
            req = urllib.request.Request(ep, data=encoded, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                return data.get('elements', [])
        except Exception as e:
            continue
    
    return None

def query_nominatim(street_name):
    """Fallback: busca via Nominatim para pegar dados extras"""
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
        'q': f'{street_name}, Perus, São Paulo',
        'format': 'json',
        'limit': '1',
        'extratags': '1'
    })
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if data and len(data) > 0:
                return data[0]
    except:
        pass
    return None

# ============ EXECUTAR ============
print("=" * 80)
print("VARREDURA DE LARGURA DAS RUAS — PERUS, SÃO PAULO")
print("=" * 80)
print()

results = []
overpass_ok = True

for street in streets_to_check:
    nome = street['nome']
    print(f"🔍 Buscando: {nome}...", end=" ", flush=True)
    
    width = None
    source = 'Sem dados'
    
    # Tentar Overpass primeiro
    if overpass_ok:
        elements = query_overpass(nome)
        if elements is None:
            print("(Overpass offline, usando Nominatim)", end=" ")
            overpass_ok = False
        elif len(elements) > 0:
            # Pegar o elemento com mais tags
            best = max(elements, key=lambda e: len(e.get('tags', {})))
            tags = best.get('tags', {})
            width, source = estimate_width(tags)
            if width:
                print(f"✅ {width}m ({source})")
            else:
                highway = tags.get('highway', '?')
                width = WIDTH_BY_HIGHWAY.get(highway, 6.0)
                source = f'Estimado (tipo: {highway})'
                print(f"📊 {width}m ({source})")
        else:
            print("❌ Não encontrada no OSM", end=" ")
    
    # Fallback Nominatim
    if width is None:
        nom = query_nominatim(nome)
        if nom and 'extratags' in nom:
            tags = nom['extratags']
            width, source = estimate_width(tags)
            if width:
                print(f"✅ {width}m ({source} via Nominatim)")
        
        if width is None:
            # Última tentativa: classificação do Nominatim
            if nom and nom.get('type') in WIDTH_BY_HIGHWAY:
                width = WIDTH_BY_HIGHWAY[nom['type']]
                source = f'Estimado (Nominatim tipo: {nom["type"]})'
                print(f"📊 {width}m ({source})")
            elif nom and nom.get('class') == 'highway':
                width = 6.0
                source = 'Padrão residencial (sem dados específicos)'
                print(f"⚠️ {width}m ({source})")
            else:
                width = street['largura_atual']
                source = 'SEM DADOS — mantém valor atual'
                print(f"⚠️ {width}m ({source})")
    
    results.append({
        'id': street['id'],
        'nome': nome,
        'largura_anterior': street['largura_atual'],
        'largura_nova': width,
        'fonte': source
    })
    
    time.sleep(1.2)  # Rate limiting

# ============ RELATÓRIO FINAL ============
print()
print("=" * 80)
print("RELATÓRIO FINAL")
print("=" * 80)
print()
print(f"{'ID':>3} | {'Rua':<30} | {'Antes':>6} | {'Nova':>6} | {'Fonte'}")
print("-" * 100)

for r in results:
    changed = '→' if r['largura_anterior'] != r['largura_nova'] else '='
    print(f"{r['id']:>3} | {r['nome']:<30} | {r['largura_anterior']:>5}m | {r['largura_nova']:>5}m {changed} | {r['fonte']}")

# Salvar JSON para uso posterior
with open('larguras_resultado.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print()
print("📁 Resultados salvos em larguras_resultado.json")
