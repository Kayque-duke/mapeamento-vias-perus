import json
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

streets = {
    'Rota 1': [
        'Rua Mar do Norte, Perus, São Paulo',
        'Rua Mar das Flores, Perus, São Paulo',
        'Rua Mar da Irlanda, Perus, São Paulo',
        'Rua Ilha de Bali, Perus, São Paulo',
        'Rua Guaratinga, Perus, São Paulo',
        'Rua Sapucainha, Perus, São Paulo',
        'Rua das Alpinas, Perus, São Paulo',
        'Rua do Cerrado Brasileiro, Perus, São Paulo'
    ],
    'Rota 2': [
        'Rua do Marajó, Jaraguá, São Paulo',
        'Rua Ilhas Britânicas, Jaraguá, São Paulo',
        'Rua Albert Jansen, Jaraguá, São Paulo'
    ],
    'Rota 3': [
        'Rua Artur de Azevedo, Jardim Nascente, São Paulo',
        'Alameda Aristoteles Claudio Sbrigh, Jardim Nascente, São Paulo',
        'Rua Ana Maria Franco Laranjeiras, Sítio Areião, São Paulo',
        'Rua Cleonice Kammer di Sandro, Sítio Areião, São Paulo'
    ],
    'Rota 4': [
        'Rua Vieira de Brito, Botuquara, São Paulo',
        'Rua Miguel Vilela, Botuquara, São Paulo'
    ],
    'Rota 5': [
        'Travessa Cambaratiba, Perus, São Paulo',
        'Rua Chamburcy, Vila Perus, São Paulo',
        'Travessa Lobito, Morro Doce, São Paulo'
    ]
}

geolocator = Nominatim(user_agent="perus_jaragua_mapper_gabriel")
results = {}

for route, vias in streets.items():
    results[route] = []
    for via in vias:
        print(f"Geocoding {via}...")
        try:
            location = geolocator.geocode(via, timeout=10)
            if location:
                results[route].append({
                    "name": via.split(",")[0],
                    "route": route,
                    "lat": location.latitude,
                    "lng": location.longitude
                })
            else:
                # Try a broader search
                broader = via.split(",")[0] + ", São Paulo"
                location = geolocator.geocode(broader, timeout=10)
                if location:
                    results[route].append({
                        "name": via.split(",")[0],
                        "route": route,
                        "lat": location.latitude,
                        "lng": location.longitude
                    })
                else:
                    results[route].append({
                        "name": via.split(",")[0],
                        "route": route,
                        "lat": None,
                        "lng": None
                    })
        except GeocoderTimedOut:
            results[route].append({
                "name": via.split(",")[0],
                "route": route,
                "lat": None,
                "lng": None
            })
        time.sleep(1.2) # Be kind to Nominatim

with open('rotas_coordenadas.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Done geocoding.")
