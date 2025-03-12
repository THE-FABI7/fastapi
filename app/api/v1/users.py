from fastapi import APIRouter, HTTPException
from typing import List
from app.models.user import UserCreate, UserResponse, UserUpdate
from app.db.database import users_collection
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["Usuarios"])

# Obtener todos los usuarios
@router.get("/", response_model=List[UserResponse])
async def get_users():
    users = await users_collection.find().to_list(100)
    return [{"id": str(user["_id"]), **user} for user in users]

# Obtener un usuario por ID
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {"id": str(user["_id"]), **user}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Crear un nuevo usuario
@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    new_user = user.dict()
    result = await users_collection.insert_one(new_user)
    new_user["id"] = str(result.inserted_id)
    return new_user

# Actualizar un usuario
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserUpdate):
    existing_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    updated_user = {k: v for k, v in user.dict(exclude_unset=True).items() if v is not None}
    await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})
    
    updated_user["id"] = user_id
    return updated_user

# Eliminar un usuario
@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado"}
