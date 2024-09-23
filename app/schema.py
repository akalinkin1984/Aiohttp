from pydantic import BaseModel


class UpdateAdv(BaseModel):
    title: str | None = None
    description: str | None = None
    owner: str | None = None


class CreateAdv(BaseModel):
    title: str
    description: str
    owner: str
