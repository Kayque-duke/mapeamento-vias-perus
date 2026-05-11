import json
import os
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
            print(f"Failed to parse {key}: {e}")
            data[key] = []
    else:
        print(f"Could not find {key}")
        data[key] = []

pinos = data.get("genio_pinos_perus_v1", [])
v17_list = data.get("genio_ruas_perus_v17", [])
v18_list = data.get("genio_ruas_perus_v18", [])

print(f"Loaded {len(pinos)} pins")
print(f"Loaded {len(v17_list)} v17 streets")
print(f"Loaded {len(v18_list)} v18 streets")

html_file = r'c:\Users\gabri\Nova pasta (3)\mapeamento_das_vias.html'
with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

v18_ids = {s['id'] for s in v18_list if 'id' in s}

merged_list = []
for s in v17_list:
    if 'id' in s and s['id'] not in v18_ids:
        merged_list.append(s)

merged_list.extend(v18_list)

merged_json = json.dumps(merged_list, separators=(",", ":"))
pinos_json = json.dumps(pinos, separators=(",", ":"))

# We must use lambda in re.sub so that backslashes in JSON (like \u) are not treated as escape sequences by re.sub
new_html = re.sub(r'let streets = \[.*?\];', lambda m: f'let streets = {merged_json};', html, flags=re.DOTALL)
new_html = re.sub(r'let userPins = \[.*?\];', lambda m: f'let userPins = {pinos_json};', new_html, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Updated streets. Total streets: {len(merged_list)} (Merged {len(v17_list)} and {len(v18_list)}). Pins: {len(pinos)}")

