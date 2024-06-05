from pydantic import BaseModel


class UserMessage(BaseModel):
    user_id: int
    truck_id: int


class TruckInfo(BaseModel):
    truck_id: int
    truck_name: str
    govNumber: str
    driver: str
