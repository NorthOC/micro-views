from pydantic import BaseModel

class Url(BaseModel):
    url: str

class Viewer(BaseModel):
    country: str | None = None
    ip: str | None = None
    client_uuid: str