import httpx
from backend.database import SUPABASE_URL, HEADERS

class PinosRepository:
    def get_all(self):
        url = f"{SUPABASE_URL}/rest/v1/pinos?select=*&order=id.asc"
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()

    def get_by_id(self, pino_id: int):
        url = f"{SUPABASE_URL}/rest/v1/pinos?id=eq.{pino_id}&select=*"
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None

    def create(self, pino_data: dict):
        url = f"{SUPABASE_URL}/rest/v1/pinos"
        response = httpx.post(url, headers=HEADERS, json=pino_data)
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None

    def update(self, pino_id: int, pino_data: dict):
        url = f"{SUPABASE_URL}/rest/v1/pinos?id=eq.{pino_id}"
        response = httpx.patch(url, headers=HEADERS, json=pino_data)
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None

    def delete(self, pino_id: int):
        url = f"{SUPABASE_URL}/rest/v1/pinos?id=eq.{pino_id}"
        response = httpx.delete(url, headers=HEADERS)
        response.raise_for_status()
        return True

pinos_repository = PinosRepository()
