from pydantic import BaseModel


class Service(BaseModel):
    title: str
    description: str
    creator_id: int
