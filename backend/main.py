from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import ruas_router, pinos_router

app = FastAPI(
    title="API Titãs - Proposta 3351",
    description="Backend em Python conectado ao Supabase para gerenciar vias e pinos do mapa.",
    version="1.0.0"
)

# Configurando CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrando os routers
app.include_router(ruas_router.router)
app.include_router(pinos_router.router)

@app.get("/")
def read_root():
    return {"message": "API Titãs (FastAPI) está rodando! Acesse /docs para ver o Swagger UI."}
