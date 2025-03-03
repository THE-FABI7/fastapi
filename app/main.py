from fastapi import FastAPI
from app.api.v1 import users

app = FastAPI(title="API de Usuarios con FastAPI")

# Registrar rutas
app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
