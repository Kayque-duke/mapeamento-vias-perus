import httpx
from backend.database import SUPABASE_URL, HEADERS

class RuasRepository:
    def get_all(self):
        url = f"{SUPABASE_URL}/rest/v1/ruas?select=*&order=id.asc"
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()

    def get_by_id(self, rua_id: int):
        url = f"{SUPABASE_URL}/rest/v1/ruas?id=eq.{rua_id}&select=*"
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None

    def create(self, rua_data: dict):
        url = f"{SUPABASE_URL}/rest/v1/ruas"
        response = httpx.post(url, headers=HEADERS, json=rua_data)
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None

    def update(self, rua_id: int, rua_data: dict):
        url = f"{SUPABASE_URL}/rest/v1/ruas?id=eq.{rua_id}"
        response = httpx.patch(url, headers=HEADERS, json=rua_data)
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None

    def delete(self, rua_id: int):
        url = f"{SUPABASE_URL}/rest/v1/ruas?id=eq.{rua_id}"
        response = httpx.delete(url, headers=HEADERS)
        response.raise_for_status()
        return True

ruas_repository = RuasRepository()
