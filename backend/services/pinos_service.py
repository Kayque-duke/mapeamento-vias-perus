from backend.repositories.pinos_repository import pinos_repository

class PinosService:
    def get_all(self):
        return pinos_repository.get_all()

    def get_by_id(self, pino_id: int):
        pino = pinos_repository.get_by_id(pino_id)
        if not pino:
            raise ValueError("Pino não encontrado.")
        return pino

    def create(self, pino_data: dict):
        if 'lat' not in pino_data or 'lng' not in pino_data:
            raise ValueError("Os campos 'lat' e 'lng' são obrigatórios.")
        return pinos_repository.create(pino_data)

    def update(self, pino_id: int, pino_data: dict):
        existente = pinos_repository.get_by_id(pino_id)
        if not existente:
            raise ValueError("Pino não encontrado.")
        return pinos_repository.update(pino_id, pino_data)

    def delete(self, pino_id: int):
        existente = pinos_repository.get_by_id(pino_id)
        if not existente:
            raise ValueError("Pino não encontrado.")
        return pinos_repository.delete(pino_id)

pinos_service = PinosService()
