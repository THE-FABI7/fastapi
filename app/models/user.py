from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str] = "user"  # Campo de rol con valor predeterminado "user"