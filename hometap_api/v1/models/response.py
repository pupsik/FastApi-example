from pydantic import BaseModel


class HasSepticSystemResponse(BaseModel):
    has_septic_system: bool


class HelloWorldResponse(BaseModel):
    hello: str
