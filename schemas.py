import validators

from typing import List
from pydantic import BaseModel, validator


class URLRequest(BaseModel):
    target_url: str

    @validator('target_url')
    def valid_url(cls, data):
        if not validators.url(data):
            raise ValueError('Provide valid url')
        return data


class URLResponse(BaseModel):
    original_url: str
    key: str
    target_url: str
    click: int

    class Config:
        orm_mode = True


class URLListResponse(BaseModel):
    data: List[URLResponse]
