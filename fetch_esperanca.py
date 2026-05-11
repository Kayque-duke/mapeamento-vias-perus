import urllib.request
import json
import urllib.parse

# Busca via Overpass API usando bounding box de Perus  
query = """
[out:json][timeout:25];
(
  way["name"~"Esperan"]["highway"](around:2000,-23.418,-46.752);
);
out body;
>;
out skel qt;
"""

url = 'https://overpass-api.de/api/interpreter'
encoded_data = urllib.parse.urlencode({'data': query.strip()}).encode('utf-8')
req = urllib.request.Request(url, data=encoded_data, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
})

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
        elements = result.get('elements', [])
        ways = [e for e in elements if e['type'] == 'way']
        nodes = {e['id']: e for e in elements if e['type'] == 'node'}
        print(f"Found {len(ways)} ways, {len(nodes)} nodes")
        for w in ways:
            name = w.get('tags', {}).get('name', 'Unknown')
            node_ids = w.get('nodes', [])
            coords = []
            for nid in node_ids:
                n = nodes.get(nid)
                if n:
                    coords.append({"lat": round(n['lat'], 7), "lng": round(n['lon'], 7)})
            print(f"\n=== {name} (way {w['id']}) ===")
            print(f"Points: {len(coords)}")
            if coords:
                print(f"Start: {coords[0]}")
                print(f"End: {coords[-1]}")
                print(f"Coords JSON:")
                print(json.dumps(coords))
except Exception as e:
    print(f"Error: {e}")
