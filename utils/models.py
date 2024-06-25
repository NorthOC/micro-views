from pydantic import BaseModel

class Url(BaseModel):
    url: str

class Viewer(BaseModel):
    country: str = None
    ip: str = None
    client_uuid: str