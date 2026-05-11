import urllib.request
import json
import urllib.parse
import time

url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote('Rua Noel Rosa, Vila dos Palmares, Sao Paulo')}&format=json&polygon_geojson=1&limit=1"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        if data and len(data) > 0:
            geojson = data[0].get('geojson', {})
            if geojson.get('type') in ['LineString', 'MultiLineString']:
                coords = geojson['coordinates']
                if geojson['type'] == 'MultiLineString': coords = coords[0]
                formatted_coords = [{"lat": c[1], "lng": c[0]} for c in coords]
                print(f"Rua Noel Rosa FOUND:")
                print(json.dumps(formatted_coords))
            else:
                print(f"Rua Noel Rosa: Not a LineString")
        else:
            print(f"Rua Noel Rosa: Not found")
except Exception as e:
    print(f"Rua Noel Rosa: Error", e)
