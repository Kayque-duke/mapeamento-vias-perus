import urllib.request
import json
import urllib.parse
import time

streets = [
    "Rua Francisco Bellazzi",
    "Avenida Felippo Sturba",
    "Rua Onze",
    "Rua Educador",
    "Rua Noel Rosa",
    "Rua Carlos Lamarca",
    "Rua Ilha da Vitória",
    "Rua Nova Vida"
]

for street in streets:
    query = f'[out:json];way["name"~"{street}",i](around:15000,-23.407,-46.756);out geom;'
    encoded_query = urllib.parse.quote(query)
    req = urllib.request.Request('https://overpass-api.de/api/interpreter?data=' + encoded_query, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data['elements']:
                for el in data['elements']:
                    if 'geometry' in el:
                        geom = el['geometry']
                        formatted_coords = [{"lat": g["lat"], "lng": g["lon"]} for g in geom]
                        print(f"\n{street} FOUND:")
                        print(json.dumps(formatted_coords))
                        break # print only the first way
            else:
                print(f"\n{street}: No elements")
    except Exception as e:
        print(f"\n{street}: Error", e)
    time.sleep(1.5)
