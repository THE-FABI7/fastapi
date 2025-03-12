from fastapi import FastAPI, HTTPException, Depends
from app.db.database import users_collection
from app.models.user import User
from bson import ObjectId
from typing import List

app = FastAPI()

@app.post("/users/")
async def create_user(user: User):
    user_dict = user.dict()
    result = await users_collection.insert_one(user_dict)
    return {"id": str(result.inserted_id)}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])  # Convertir ObjectId a string
    return user

@app.get("/users/")
async def get_users():
    users = []
    async for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    await users_collection.delete_one({"_id": ObjectId(user_id)})
    return {"message": "User deleted successfully"}

# Middleware o dependencia para verificar roles
async def get_current_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def verify_role(user_id: str, required_role: str):
    user = await get_current_user(user_id)
    if user["role"] != required_role:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return user

@app.get("/admin/users/", dependencies=[Depends(lambda: verify_role(user_id="some_user_id", required_role="admin"))])
async def get_all_users():
    users = []
    async for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@app.post("/admin/users/")
async def create_admin_user(user: User, current_user: User = Depends(lambda: verify_role(user_id="some_user_id", required_role="admin"))):
    user_dict = user.dict()
    user_dict["role"] = "admin"  # Asignar rol de administrador
    result = await users_collection.insert_one(user_dict)
    return {"id": str(result.inserted_id)}