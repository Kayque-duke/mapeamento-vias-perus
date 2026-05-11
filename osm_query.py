import urllib.request
import json
import urllib.parse

query = '[out:json];way["name"~"Estrada de Pirapora",i](around:15000,-23.407,-46.756);out geom;'
encoded_query = urllib.parse.quote(query)
req = urllib.request.Request('https://overpass-api.de/api/interpreter?data=' + encoded_query)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        if data['elements']:
            for el in data['elements']:
                if 'geometry' in el:
                    geom = el['geometry']
                    print(f"ID: {el['id']}")
                    for g in geom[:5]:
                        print(f"  {g['lat']}, {g['lon']}")
        else:
            print('No elements found')
except Exception as e:
    print(e)
