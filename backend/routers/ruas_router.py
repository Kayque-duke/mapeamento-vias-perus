from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from backend.services.ruas_service import ruas_service

router = APIRouter(prefix="/api/ruas", tags=["Ruas"])

class RuaSchema(BaseModel):
    id: Optional[int] = None
    nome: Optional[str] = None
    bairro: Optional[str] = None
    tipo: Optional[str] = None
    inicio: Optional[str] = None
    fim: Optional[str] = None
    largura: Optional[float] = None
    pavimento: Optional[str] = None
    comprimento_manual: Optional[float] = None
    obs: Optional[str] = None
    has_photos: Optional[bool] = False
    coords: Optional[List[Any]] = []
    
    class Config:
        extra = "allow"

@router.get("/")
def get_all_ruas():
    try:
        return ruas_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{rua_id}")
def get_rua(rua_id: int):
    try:
        return ruas_service.get_by_id(rua_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_rua(rua: RuaSchema):
    try:
        rua_dict = rua.model_dump(exclude_unset=True)
        return ruas_service.create(rua_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{rua_id}")
def update_rua(rua_id: int, rua: RuaSchema):
    try:
        rua_dict = rua.model_dump(exclude_unset=True)
        return ruas_service.update(rua_id, rua_dict)
    except ValueError as e:
        if "não encontrada" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{rua_id}")
def delete_rua(rua_id: int):
    try:
        ruas_service.delete(rua_id)
        return {"message": "Rua deletada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
