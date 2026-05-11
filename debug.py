import json
import re

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

with open('lista_ruas.md', 'w', encoding='utf-8') as f:
    f.write(f"### Ruas Mapeadas ({len(merged_list)})\n\n")
    for s in merged_list:
        f.write(f"- {s.get('nome', 'Sem nome')}\n")
    
    f.write(f"\n### Pinos Adicionados ({len(pinos)})\n\n")
    for p in pinos:
        f.write(f"- {p.get('name', 'Sem nome')}\n")

print("Generated lista_ruas.md")


