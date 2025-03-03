from fastapi import APIRouter, HTTPException
from typing import List
from app.models.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Usuarios"])

# Base de datos simulada
fake_users_db = []

# Obtener todos los usuarios
@router.get("/", response_model=List[UserResponse])
def get_users():
    return fake_users_db

# Obtener un usuario por ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Crear un nuevo usuario
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    new_user = {"id": len(fake_users_db) + 1, **user.dict()}
    fake_users_db.append(new_user)
    return new_user

# Actualizar un usuario
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate):
    for idx, existing_user in enumerate(fake_users_db):
        if existing_user["id"] == user_id:
            updated_user = existing_user | user.dict(exclude_unset=True)
            fake_users_db[idx] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Eliminar un usuario
@router.delete("/{user_id}")
def delete_user(user_id: int):
    global fake_users_db
    fake_users_db = [user for user in fake_users_db if user["id"] != user_id]
    return {"message": "Usuario eliminado"}
