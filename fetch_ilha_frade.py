import urllib.request
import json
import urllib.parse

# Try Nominatim first
url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
    'q': 'Rua Ilha do Frade, Perus, São Paulo',
    'format': 'json',
    'polygon_geojson': '1',
    'limit': '5'
})

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0'
})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
        print(f"Nominatim results: {len(data)}")
        for item in data:
            name = item.get('display_name', '')
            geojson = item.get('geojson', {})
            gtype = geojson.get('type', 'N/A')
            print(f"\n  Name: {name}")
            print(f"  Type: {gtype}")
            print(f"  Lat: {item.get('lat')}, Lon: {item.get('lon')}")
            if gtype in ['LineString', 'MultiLineString']:
                coords_raw = geojson['coordinates']
                if gtype == 'MultiLineString':
                    coords_raw = coords_raw[0]
                coords = [{"lat": round(c[1], 7), "lng": round(c[0], 7)} for c in coords_raw]
                print(f"  Points: {len(coords)}")
                print(f"  Start: {coords[0]}")
                print(f"  End:   {coords[-1]}")
                print(f"  Coords: {json.dumps(coords)}")
            else:
                print(f"  GeoJSON coords: {json.dumps(geojson.get('coordinates', []))}")
except Exception as e:
    print(f"Nominatim error: {e}")

# Also try without accent
print("\n\n--- Second attempt without accent ---")
url2 = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
    'q': 'Rua Ilha do Frade, Sao Paulo',
    'format': 'json',
    'polygon_geojson': '1',
    'limit': '5'
})

import time
time.sleep(1.5)

req2 = urllib.request.Request(url2, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0'
})

try:
    with urllib.request.urlopen(req2, timeout=15) as resp2:
        data2 = json.loads(resp2.read().decode())
        print(f"Nominatim results: {len(data2)}")
        for item in data2:
            name = item.get('display_name', '')
            geojson = item.get('geojson', {})
            gtype = geojson.get('type', 'N/A')
            print(f"\n  Name: {name}")
            print(f"  Type: {gtype}")
            print(f"  Lat: {item.get('lat')}, Lon: {item.get('lon')}")
            if gtype in ['LineString', 'MultiLineString']:
                coords_raw = geojson['coordinates']
                if gtype == 'MultiLineString':
                    coords_raw = coords_raw[0]
                coords = [{"lat": round(c[1], 7), "lng": round(c[0], 7)} for c in coords_raw]
                print(f"  Points: {len(coords)}")
                print(f"  Start: {coords[0]}")
                print(f"  End:   {coords[-1]}")
                print(f"  Coords: {json.dumps(coords)}")
except Exception as e:
    print(f"Nominatim error: {e}")
