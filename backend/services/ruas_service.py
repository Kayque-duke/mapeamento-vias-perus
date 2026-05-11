from backend.repositories.ruas_repository import ruas_repository

class RuasService:
    def get_all(self):
        return ruas_repository.get_all()

    def get_by_id(self, rua_id: int):
        rua = ruas_repository.get_by_id(rua_id)
        if not rua:
            raise ValueError("Rua não encontrada.")
        return rua

    def create(self, rua_data: dict):
        if 'nome' not in rua_data or not rua_data['nome']:
            raise ValueError("O campo 'nome' é obrigatório.")
        # Adicione regras de negócio adicionais aqui se necessário
        return ruas_repository.create(rua_data)

    def update(self, rua_id: int, rua_data: dict):
        existente = ruas_repository.get_by_id(rua_id)
        if not existente:
            raise ValueError("Rua não encontrada.")
        return ruas_repository.update(rua_id, rua_data)

    def delete(self, rua_id: int):
        existente = ruas_repository.get_by_id(rua_id)
        if not existente:
            raise ValueError("Rua não encontrada.")
        return ruas_repository.delete(rua_id)

ruas_service = RuasService()
