from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from backend.services.pinos_service import pinos_service

router = APIRouter(prefix="/api/pinos", tags=["Pinos"])

class PinoSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    color: Optional[str] = None
    lat: float
    lng: float
    
    class Config:
        extra = "allow"

@router.get("/")
def get_all_pinos():
    try:
        return pinos_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{pino_id}")
def get_pino(pino_id: int):
    try:
        return pinos_service.get_by_id(pino_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_pino(pino: PinoSchema):
    try:
        pino_dict = pino.model_dump(exclude_unset=True)
        return pinos_service.create(pino_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{pino_id}")
def update_pino(pino_id: int, pino: PinoSchema):
    try:
        pino_dict = pino.model_dump(exclude_unset=True)
        return pinos_service.update(pino_id, pino_dict)
    except ValueError as e:
        if "não encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{pino_id}")
def delete_pino(pino_id: int):
    try:
        pinos_service.delete(pino_id)
        return {"message": "Pino deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
