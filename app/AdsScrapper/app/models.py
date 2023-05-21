from enum import Enum
from pydantic import BaseModel, Field


class UrlTypes(str, Enum):
    GOOGLE = "https://www.google.com/"


class InputDataBrowser(BaseModel):
    url: str
    search: str
    query: str
    user_agent: str = Field(..., alias="user-agent")
    context: str


class InputDataSite(BaseModel):
    url: str
    query: str
    user_agent: str = Field(..., alias="user-agent")
    context: str


class ResponseData(BaseModel):
    url: str
    user_agent: str
    context: str
    ads: dict
