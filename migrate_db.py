import json
import re
import requests

# Supabase Credentials
SUPABASE_URL = "https://ozoafprfhmtgwqqevzgv.supabase.co"
SUPABASE_KEY = "sb_publishable_wRIpRjFI1-CJUkUJMqqq3w_fI4PqfeP"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

print("Lendo dados locais...")
with open('dados.json', 'r', encoding='utf-8') as f:
    raw_json = f.read()

data = {}
for key in ["genio_pinos_perus_v1", "genio_ruas_perus_v17", "genio_ruas_perus_v18"]:
    match = re.search(r'"' + key + r'"\s*:\s*"(.*?)(?<!\\)"\s*(?:,|}|\n|$)', raw_json)
    if match:
        s = match.group(1).replace('\\"', '"').replace('\\\\', '\\')
        try:
            data[key] = json.loads(s)
        except Exception as e:
            data[key] = []
    else:
        data[key] = []

pinos = data.get("genio_pinos_perus_v1", [])
v17_list = data.get("genio_ruas_perus_v17", [])
v18_list = data.get("genio_ruas_perus_v18", [])

v18_ids = {s.get('id') for s in v18_list if s.get('id')}
merged_list = [s for s in v17_list if s.get('id') not in v18_ids] + v18_list

print(f"Total de Ruas a migrar: {len(merged_list)}")
print(f"Total de Pinos a migrar: {len(pinos)}")

def upload_ruas():
    # Format data for database
    ruas_db = []
    for s in merged_list:
        rua = {
            "id": s.get("id"),
            "nome": s.get("nome"),
            "bairro": s.get("bairro"),
            "tipo": s.get("tipo"),
            "inicio": s.get("inicio"),
            "fim": s.get("fim"),
            "largura": s.get("largura") if s.get("largura") not in ["", None] else None,
            "pavimento": s.get("pavimento", ""),
            "comprimento_manual": s.get("comprimentoManual") if s.get("comprimentoManual") not in ["", None] else None,
            "obs": s.get("obs", ""),
            "has_photos": s.get("hasPhotos", False),
            "coords": s.get("coords", [])
        }
        ruas_db.append(rua)
    
    print("Enviando Ruas para o Supabase...")
    # Upsert (insert or update)
    headers = HEADERS.copy()
    headers["Prefer"] = "resolution=merge-duplicates,return=representation"
    
    response = requests.post(f"{SUPABASE_URL}/rest/v1/ruas", headers=headers, json=ruas_db)
    if response.status_code in [200, 201]:
        print("Sucesso: Ruas enviadas!")
    else:
        print(f"Erro ao enviar ruas: {response.status_code} - {response.text}")

def upload_pinos():
    pinos_db = []
    for p in pinos:
        pino = {
            "name": p.get("name"),
            "color": p.get("color"),
            "lat": p.get("lat"),
            "lng": p.get("lng")
        }
        pinos_db.append(pino)
    
    print("Enviando Pinos para o Supabase...")
    response = requests.post(f"{SUPABASE_URL}/rest/v1/pinos", headers=HEADERS, json=pinos_db)
    if response.status_code in [200, 201]:
        print("Sucesso: Pinos enviados!")
    else:
        print(f"Erro ao enviar pinos: {response.status_code} - {response.text}")

# First try to see if requests exists
try:
    upload_ruas()
    upload_pinos()
except Exception as e:
    print(f"Erro inesperado: {e}")
