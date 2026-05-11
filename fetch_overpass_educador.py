import urllib.request
import json
import urllib.parse

query = '[out:json];(way["name"~"Educador|Noel Rosa",i](around:2000,-23.4285,-46.7766););out geom;'
encoded_query = urllib.parse.quote(query)
req = urllib.request.Request('https://overpass-api.de/api/interpreter?data=' + encoded_query, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        if data.get('elements'):
            for el in data['elements']:
                name = el.get('tags', {}).get('name', 'Unknown')
                if 'geometry' in el:
                    formatted_coords = [{"lat": g["lat"], "lng": g["lon"]} for g in el['geometry']]
                    print(f"\n{name} FOUND:")
                    print(json.dumps(formatted_coords))
        else:
            print("No elements found")
except Exception as e:
    print("Error", e)
