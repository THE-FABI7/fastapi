from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://user_eventos:Woexhjvql7GYe3ea@tallerprog3.7h2ert5.mongodb.net")
DATABASE_NAME = "fastapi"

try:
    client = AsyncIOMotorClient(MONGO_URI)
    database = client[DATABASE_NAME]
    users_collection = database["users"]
    database.list_collection_names()
    print("Conexión exitosa")
except Exception as e:
    print(f"Error: {e}")