from pydantic import BaseModel, EmailStr

class SPlanSubscription(BaseModel):
    id: int
    name: str
    price: float
    duration_days: int

    class Config:
        from_attributes = True
