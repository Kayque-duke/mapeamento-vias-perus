import http.client
import json
import urllib.parse

query = '[out:json];way["name"~"Noel Rosa"](around:5000,-23.4396,-46.8084);out geom;'
encoded_query = urllib.parse.quote(query)

conn = http.client.HTTPSConnection("overpass-api.de")
headers = {
    'User-Agent': 'Mozilla/5.0'
}
conn.request("GET", "/api/interpreter?data=" + encoded_query, headers=headers)
res = conn.getresponse()
data = res.read()
try:
    j = json.loads(data.decode('utf-8'))
    for el in j.get('elements', []):
        if 'geometry' in el:
            coords = [{"lat": g["lat"], "lng": g["lon"]} for g in el['geometry']]
            print("Rua Noel Rosa FOUND:")
            print(json.dumps(coords))
            break
except Exception as e:
    print(e)
