from pydantic import BaseModel

class UserLogin(BaseModel):
    login: str
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    role: str

    class Config:
        from_attributes = True