import urllib.request
import json
import urllib.parse

query = '[out:json];(way["name"~"Felippo Sturba"](around:5000,-23.424,-46.756););out geom;'
encoded_query = urllib.parse.quote(query)

req = urllib.request.Request('https://overpass-api.de/api/interpreter?data=' + encoded_query, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        if data.get('elements'):
            for el in data['elements']:
                name = el.get('tags', {}).get('name', 'Unknown')
                print(f"FOUND: {name}")
                if 'geometry' in el:
                    print(el['geometry'][:2])
        else:
            print("No elements found")
except Exception as e:
    print("Error", e)
